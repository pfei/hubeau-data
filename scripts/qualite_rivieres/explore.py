from typing import Any, Dict, List

import httpx

from scripts.qualite_rivieres.api_utils import fetch_analyses, fetch_stations

# Define endpoints
ENDPOINTS = {
    "analyse_pc": ("https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/analyse_pc"),
    "condition_environnementale_pc": (
        "https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/condition_environnementale_pc"
    ),
    "operation_pc": (
        "https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/operation_pc"
    ),
    "station_pc": ("https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/station_pc"),
}


def get_endpoint_summary(
    endpoint: str, url: str, sample_size: int = 1
) -> Dict[str, Any]:
    """Fetch a summary of an endpoint: count and a sample record."""
    try:
        resp = httpx.get(url, params={"size": sample_size})
        resp.raise_for_status()
        data = resp.json()
        sample_data = data.get("data", [])
        return {
            "endpoint": endpoint,
            "count": data.get("count", 0),
            "sample_record": sample_data[0] if sample_data else None,
        }
    except Exception as e:
        return {
            "endpoint": endpoint,
            "error": str(e),
        }


def summarize_endpoints(
    endpoints: Dict[str, str], sample_size: int = 1
) -> List[Dict[str, Any]]:
    """Summarize all endpoints."""
    return [
        get_endpoint_summary(name, url, sample_size) for name, url in endpoints.items()
    ]


def print_sample_record(summaries: List[Dict[str, Any]], endpoint: str) -> None:
    summary = next(s for s in summaries if s["endpoint"] == endpoint)
    print(f"Sample record for {endpoint}:")
    print(summary["sample_record"])


def main() -> None:
    print("Fetching stations...")
    try:
        stations = fetch_stations(10)
        print(f"Found {len(stations)} stations.")

        if not stations:
            print("No stations found.")
            return

        for station in stations:
            if station.code_station is None:
                print(
                    f"\nStation: {station.libelle_station} "
                    f"(code: None) - Skipping, no code_station"
                )
                continue
            try:
                analyses = list(fetch_analyses(station.code_station))
                print(
                    f"\nStation: {station.libelle_station} "
                    f"(code: {station.code_station})"
                )
                print(f"Number of analyses: {len(analyses)}")
                if analyses:
                    print("First analysis parameter:", analyses[0].libelle_parametre)
            except Exception as e:
                print(
                    f"Error fetching analyses for station {station.code_station}: {e}"
                )
    except Exception as e:
        print(f"Error fetching stations: {e}")


if __name__ == "__main__":
    main()
