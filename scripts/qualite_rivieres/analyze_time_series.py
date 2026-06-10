#!/usr/bin/env python3
"""Analyze time series availability in the Qualité Rivières API.

For a sample of stations, fetches analyses and identifies which parameters
have enough temporal coverage to be used for time series analysis.

Results are saved incrementally to data/exploration/qualite_rivieres/.

Usage:
    uv run python scripts/qualite_rivieres/analyze_time_series.py
"""

import csv
import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Iterator, cast

from hubeau_data.client import HubeauClient
from hubeau_data.models.qualite_rivieres import (
    AnalysePcParams,
    StationPc,
    StationPcParams,
)

# --- Configuration ---
OUTPUT_DIR = Path("data/exploration/qualite_rivieres")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

NUM_STATIONS = 5
MAX_ANALYSES_PER_STATION = 5000
BATCH_SIZE = 100

logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s %(levelname)s %(message)s"
)
logger = logging.getLogger(__name__)

client = HubeauClient()


# --- Data fetching ---


def fetch_station_sample(n: int) -> list[StationPc]:
    """Fetch a sample of stations from the API."""
    return client.qualite_rivieres.get_stations(
        params=StationPcParams(size=n, sort="asc")
    )


def stream_analyses(
    code_station: str, max_records: int, batch_size: int
) -> Iterator[dict[str, Any]]:
    """Stream raw analyses for a station, up to max_records."""
    fetched = 0
    page = 1
    while fetched < max_records:
        remaining = min(batch_size, max_records - fetched)
        params = AnalysePcParams(
            code_station=[code_station],
            size=remaining,
        )
        # inject page manually via extra="allow"
        raw_params = params.model_dump(exclude_none=True)
        raw_params["page"] = page

        import httpx

        url = "https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/analyse_pc"
        try:
            resp = httpx.get(url, params=raw_params, timeout=30)
            resp.raise_for_status()
        except Exception as e:
            logger.error(
                "Error fetching analyses for %s page %d: %s", code_station, page, e
            )
            break

        data: list[dict[str, Any]] = resp.json().get("data", [])
        if not data:
            break

        yield from data
        fetched += len(data)

        if len(data) < remaining:
            break
        page += 1


# --- Analysis ---


def build_param_stats(
    code_station: str,
    max_records: int = MAX_ANALYSES_PER_STATION,
    batch_size: int = BATCH_SIZE,
) -> dict[str, Any]:
    """Build per-parameter time coverage stats for a station."""
    param_dates: dict[str, list[datetime]] = {}
    count = 0

    for item in stream_analyses(code_station, max_records, batch_size):
        count += 1
        param = item.get("libelle_parametre")
        date_str = item.get("date_prelevement")
        resultat = item.get("resultat")

        if not param or not date_str or resultat in (None, 0, "0", ""):
            continue

        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            continue

        param_dates.setdefault(param, []).append(date)

    candidates = []
    for param, dates in param_dates.items():
        if not dates:
            continue
        min_date = min(dates)
        max_date = max(dates)
        candidates.append(
            {
                "parameter": param,
                "n_measurements": len(dates),
                "min_date": min_date.date().isoformat(),
                "max_date": max_date.date().isoformat(),
                "time_span_days": (max_date - min_date).days,
            }
        )

    candidates.sort(key=lambda x: cast(int, x["n_measurements"]), reverse=True)
    return {"analysis_count": count, "candidates": candidates}


# --- Output ---


def append_json(path: Path, record: dict[str, Any]) -> None:
    records: list[dict[str, Any]] = []
    if path.exists():
        try:
            records = json.loads(path.read_text())
        except json.JSONDecodeError:
            pass
    records.append(record)
    path.write_text(json.dumps(records, indent=2))


def append_csv(
    path: Path, station: StationPc, candidates: list[dict[str, Any]]
) -> None:
    write_header = not path.exists()
    with open(path, "a", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "station_code",
                "station_name",
                "parameter",
                "n_measurements",
                "min_date",
                "max_date",
                "time_span_days",
            ],
            delimiter=";",
        )
        if write_header:
            writer.writeheader()
        for c in candidates:
            writer.writerow(
                {
                    "station_code": station.code_station,
                    "station_name": station.libelle_station,
                    **c,
                }
            )


# --- Main ---


def main() -> None:
    json_out = OUTPUT_DIR / "tsa_analysis.json"
    csv_out = OUTPUT_DIR / "tsa_analysis.csv"

    print(f"Fetching {NUM_STATIONS} stations...")
    stations = fetch_station_sample(NUM_STATIONS)
    print(f"Found {len(stations)} stations.\n")

    for station in stations:
        if not station.code_station:
            continue

        print(f"Processing {station.code_station} — {station.libelle_station}")
        stats = build_param_stats(station.code_station)

        record = {
            "station_code": station.code_station,
            "station_name": station.libelle_station,
            "analysis_count": stats["analysis_count"],
            "candidates": stats["candidates"],
        }
        append_json(json_out, record)
        append_csv(csv_out, station, stats["candidates"])

        top = stats["candidates"][:3]
        for c in top:
            print(
                f"  {c['parameter']}: {c['n_measurements']} pts "
                f"({c['min_date']} → {c['max_date']})"
            )
        print()

        time.sleep(0.5)

    print(f"Results saved to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
