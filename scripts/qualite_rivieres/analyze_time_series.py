import json
import logging
import os
import random
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

from hubeau_data.models.qualite_rivieres import StationPc
from scripts.qualite_rivieres.api_utils import fetch_analyses

# --- Configuration ---
OUTPUT_DIR = Path("data/exploration/qualite_rivieres")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = OUTPUT_DIR / "station_tsa.log"

# Analysis limits
MAX_ANALYSES_PER_STATION = 30000
NUM_STATIONS_TO_ANALYZE = 3

# File size limits (in bytes)
MAX_JSON_SIZE = 20 * 1024 * 1024 * 1024  # 20GB
MAX_CSV_SIZE = 20 * 1024 * 1024 * 1024  # 20GB

# --- Minimal logging setup ---
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.WARNING,  # Only log warnings and errors
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("explore")


def get_next_file_number(base_path: Path, extension: str) -> int:
    """Get the next available file number for rotation."""
    existing_files = list(base_path.glob(f"*{extension}"))
    if not existing_files:
        return 1
    numbers = [
        int(f.stem.split("_")[-1])
        for f in existing_files
        if f.stem.split("_")[-1].isdigit()
    ]
    return max(numbers, default=0) + 1


def get_current_output_files() -> tuple[Path, Path]:
    """Get the current output files, creating new ones if needed."""
    json_file = OUTPUT_DIR / "tsa_analysis.json"
    csv_file = OUTPUT_DIR / "tsa_analysis.csv"

    # Check if files exist and their sizes
    if json_file.exists() and os.path.getsize(json_file) >= MAX_JSON_SIZE:
        next_num = get_next_file_number(OUTPUT_DIR, ".json")
        json_file = OUTPUT_DIR / f"tsa_analysis_{next_num}.json"

    if csv_file.exists() and os.path.getsize(csv_file) >= MAX_CSV_SIZE:
        next_num = get_next_file_number(OUTPUT_DIR, ".csv")
        csv_file = OUTPUT_DIR / f"tsa_analysis_{next_num}.csv"

    return json_file, csv_file


def save_results_incrementally(
    results: List[Dict[str, Any]], json_file: Path, csv_file: Path
) -> None:
    """Save results incrementally to both JSON and CSV files."""
    # Save to JSON
    try:
        if json_file.exists() and json_file.stat().st_size > 0:
            with open(json_file, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
            existing_data.extend(results)
        else:
            existing_data = results
    except json.JSONDecodeError:
        # If the file is corrupted or empty, start fresh
        existing_data = results

    # Convert Pydantic models to dicts before JSON serialization
    serializable_data = []
    for item in existing_data:
        serializable_item = item.copy()
        if isinstance(item["station"], StationPc):
            serializable_item["station"] = item["station"].model_dump(exclude_none=True)
        serializable_data.append(serializable_item)

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(serializable_data, f, indent=2)

    # Save to CSV
    rows: List[Dict[str, Any]] = []
    for res in results:
        station_data = (
            res["station"].model_dump(exclude_none=True)
            if isinstance(res["station"], StationPc)
            else res["station"]
        )
        for cand in res.get("tsa_candidates", []):
            rows.append(
                {
                    "station_code": station_data.get("code_station"),
                    "station_name": station_data.get("libelle_station"),
                    "parameter": cand["parameter"],
                    "n_measurements": cand["n_measurements"],
                    "min_date": cand["min_date"],
                    "max_date": cand["max_date"],
                    "time_span_days": cand["time_span_days"],
                }
            )

    df = pd.DataFrame(rows)
    if csv_file.exists():
        df.to_csv(csv_file, mode="a", header=False, sep=";", index=False)
    else:
        df.to_csv(csv_file, sep=";", index=False)


# --- Worker function ---
def process_station(
    station: StationPc, debug_limit: Optional[int] = None
) -> Dict[str, Any]:
    station_id = station.code_station or "unknown"
    try:
        if station.code_station is None:
            return {
                "station": station,  # Pydantic model is JSON serializable by default
                "status": "error",
                "error": "No code_station",
                "tsa_candidates": [],
            }

        # Use a streaming approach to process analyses
        param_dates: Dict[str, List[datetime]] = {}
        param_counts: Dict[str, int] = {}
        analysis_count = 0
        save_interval = 1000  # Save every 1000 analyses

        # Process analyses one at a time
        for analysis in fetch_analyses(
            station.code_station, batch_size=1000, debug_limit=debug_limit
        ):
            analysis_count += 1
            if analysis.libelle_parametre is None:
                continue
            if getattr(analysis, "resultat", None) in (None, 0, "0", ""):
                continue

            param = analysis.libelle_parametre
            if param not in param_dates:
                param_dates[param] = []
                param_counts[param] = 0

            if analysis.date_prelevement is not None:
                try:
                    date = datetime.strptime(analysis.date_prelevement, "%Y-%m-%d")
                    param_dates[param].append(date)
                    param_counts[param] += 1
                except ValueError:
                    continue

            # Save intermediate results periodically
            if analysis_count % save_interval == 0:
                print(
                    f"Processed {analysis_count} analyses for station {station_id}, "
                    " saving intermediate results..."
                )
                intermediate_candidates = []
                for param, dates in param_dates.items():
                    if not dates:
                        continue
                    min_date = min(dates)
                    max_date = max(dates)
                    intermediate_candidates.append(
                        {
                            "parameter": param,
                            "n_measurements": param_counts[param],
                            "min_date": min_date.isoformat(),
                            "max_date": max_date.isoformat(),
                            "time_span_days": (max_date - min_date).days,
                        }
                    )
                result = {
                    "station": station,
                    "status": "in_progress",
                    "analysis_count": analysis_count,
                    "tsa_candidates": intermediate_candidates,
                }
                json_file, csv_file = get_current_output_files()
                save_results_incrementally([result], json_file, csv_file)

        # Generate final time series candidates from all collected dates
        tsa_candidates: List[Dict[str, Any]] = []
        for param, dates in param_dates.items():
            if not dates:
                continue
            min_date = min(dates)
            max_date = max(dates)
            tsa_candidates.append(
                {
                    "parameter": param,
                    "n_measurements": param_counts[param],
                    "min_date": min_date.isoformat(),
                    "max_date": max_date.isoformat(),
                    "time_span_days": (max_date - min_date).days,
                }
            )

        return {
            "station": station,  # Pydantic model is JSON serializable by default
            "status": "ok",
            "analysis_count": analysis_count,
            "tsa_candidates": tsa_candidates,
        }
    except Exception as e:
        logger.error(f"Error processing station {station_id}: {e}")
        return {
            "station": station,  # Pydantic model is JSON serializable by default
            "status": "error",
            "error": str(e),
            "tsa_candidates": [],
        }


# --- Reporting ---
def save_report(results: List[Dict[str, Any]], output_dir: Path) -> None:
    """Save the analysis results to JSON and CSV files."""
    # Convert Pydantic models to dicts before JSON serialization
    serializable_results = []
    for res in results:
        serializable_res = res.copy()
        if isinstance(res["station"], StationPc):
            serializable_res["station"] = res["station"].model_dump(exclude_none=True)
        serializable_results.append(serializable_res)

    with open(output_dir / "tsa_analysis.json", "w", encoding="utf-8") as f:
        json.dump(serializable_results, f, indent=2)

    rows: List[Dict[str, Any]] = []
    for res in results:
        station_data = (
            res["station"].model_dump(exclude_none=True)
            if isinstance(res["station"], StationPc)
            else res["station"]
        )
        for cand in res.get("tsa_candidates", []):
            rows.append(
                {
                    "station_code": station_data.get("code_station"),
                    "station_name": station_data.get("libelle_station"),
                    "parameter": cand["parameter"],
                    "n_measurements": cand["n_measurements"],
                    "min_date": cand["min_date"],
                    "max_date": cand["max_date"],
                    "time_span_days": cand["time_span_days"],
                }
            )
    df = pd.DataFrame(rows)
    df.to_csv(output_dir / "tsa_analysis.csv", sep=";", index=False)


# --- Fetch all stations ---
def fetch_all_stations(total: int, batch_size: int = 1000) -> List[StationPc]:
    import httpx

    url = "https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/station_pc"
    stations: List[StationPc] = []
    for start in range(0, total, batch_size):
        print(f"Fetching stations {start} to {min(start + batch_size, total) - 1}...")
        try:
            resp = httpx.get(
                url, params={"start": start, "size": batch_size}, timeout=60
            )
            resp.raise_for_status()
            data = resp.json()
            # Only take the stations we need up to the total limit
            remaining = total - len(stations)
            if remaining <= 0:
                break
            new_stations = [StationPc(**s) for s in data["data"][:remaining]]
            stations.extend(new_stations)
            print(f"Fetched {len(stations)} stations so far.")
            if len(stations) >= total:
                break
        except Exception as e:
            logger.error(f"Error fetching stations batch {start}: {e}")
            continue
    return stations[:total]  # Ensure we don't return more than requested


def get_total_station_count() -> int:
    import httpx

    url = "https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/station_pc"
    try:
        resp = httpx.get(url, params={"size": 1}, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        return int(data["count"])
    except Exception as e:
        logger.error(f"Error getting station count: {e}")
        return 0


def get_random_stations(
    total_stations: int, num_stations: int = NUM_STATIONS_TO_ANALYZE
) -> List[int]:
    """Get random station indices to analyze."""
    return random.sample(range(total_stations), num_stations)


def fetch_stations_by_indices(
    indices: List[int], batch_size: int = 100
) -> List[StationPc]:
    """Fetch only specific stations by their indices."""
    import httpx

    url = "https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/station_pc"
    stations: List[StationPc] = []

    # Sort indices to optimize fetching
    sorted_indices = sorted(indices)

    # Calculate which batches we need to fetch
    needed_batches = set(idx // batch_size for idx in sorted_indices)

    for batch_start in needed_batches:
        start = batch_start * batch_size
        print(f"Fetching stations {start} to {start + batch_size - 1}...")
        try:
            resp = httpx.get(
                url, params={"start": start, "size": batch_size}, timeout=60
            )
            resp.raise_for_status()
            data = resp.json()
            batch_stations = [StationPc(**item) for item in data["data"]]

            # Only keep stations we need from this batch
            for idx in sorted_indices:
                if start <= idx < start + batch_size:
                    relative_idx = idx - start
                    if relative_idx < len(batch_stations):
                        stations.append(batch_stations[relative_idx])
                        print(
                            f"Found station {batch_stations[relative_idx].code_station}"
                        )

        except Exception as e:
            logger.error(f"Error fetching stations batch {start}: {e}")
            raise

    if len(stations) != len(indices):
        missing = set(indices) - {i for i, _ in enumerate(stations)}
        logger.warning(
            f"Could not fetch all requested stations. Missing indices: {missing}"
        )

    return stations


def main() -> None:
    """Main function to analyze time series data from stations."""
    try:
        # Get total number of stations
        total_stations = get_total_station_count()
        print(f"\nTotal stations available: {total_stations}")

        # Get random station indices
        station_indices = get_random_stations(total_stations)
        print(
            f"\nRandomly selecting {NUM_STATIONS_TO_ANALYZE} stations "
            f"out of {total_stations} total stations..."
        )

        # Fetch only the selected stations
        selected_stations = fetch_stations_by_indices(station_indices)

        # Print selected station details
        print("\nSelected stations:")
        for i, station in enumerate(selected_stations, 1):
            print(
                f"{i}. Station code: {station.code_station} - "
                f"Name: {station.libelle_station}"
            )

        print(
            f"\nStarting analysis (limited to {MAX_ANALYSES_PER_STATION} "
            "analyses per station)..."
        )

        results: List[Dict[str, Any]] = []
        for station in selected_stations:
            print(
                f"\nProcessing station {station.code_station} "
                f"({station.libelle_station})..."
            )
            result = process_station(station, debug_limit=MAX_ANALYSES_PER_STATION)
            results.append(result)

            # Save results after each station
            json_file, csv_file = get_current_output_files()
            save_results_incrementally([result], json_file, csv_file)

            # Add a small delay between stations to avoid overwhelming the API
            time.sleep(1)

        # Save final report
        save_report(results, OUTPUT_DIR)
        print("\nAnalysis complete. Results saved to:", OUTPUT_DIR)

    except Exception as e:
        logger.error(f"Error in main: {e}")
        raise


if __name__ == "__main__":
    main()
