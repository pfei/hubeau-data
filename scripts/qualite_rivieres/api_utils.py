import logging
from typing import Iterator, List, Optional

import httpx

from hubeau_data.models.qualite_rivieres import AnalysePc, StationPc

logger = logging.getLogger(__name__)

ENDPOINTS = {
    "station_pc": "https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/station_pc",
    "analyse_pc": "https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/analyse_pc",
}


def fetch_stations(size: int = 10) -> List[StationPc]:
    """Fetch a sample of stations."""
    url = ENDPOINTS["station_pc"]
    resp = httpx.get(url, params={"size": size}, timeout=60)
    resp.raise_for_status()
    data = resp.json().get("data", [])
    return [StationPc(**station) for station in data]


def fetch_analyses(
    station_code: str, batch_size: int = 1000, debug_limit: Optional[int] = None
) -> Iterator[AnalysePc]:
    """Fetch analyses for a station one at a time using an iterator.

    This function yields individual AnalysePc objects instead of
    accumulating them in memory.

    Each analysis is yielded as soon as it's fetched and processed.

    Args:
        station_code: The code of the station to fetch analyses for
        batch_size: Number of analyses to fetch per API call
        debug_limit: If set, limits the total number of analyses fetched (for debugging)
    """
    url = ENDPOINTS["analyse_pc"]
    start = 0
    total_fetched = 0

    while True:
        if debug_limit is not None and total_fetched >= debug_limit:
            print(
                f"Debug limit of {debug_limit} analyses reached "
                f"for station {station_code}"
            )
            break

        print(
            f"Fetching analyses for station {station_code}, "
            f"batch {start} to {start + batch_size - 1}..."
        )

        try:
            resp = httpx.get(
                url,
                params={
                    "code_station": station_code,
                    "size": batch_size,
                    "start": start,
                },
                timeout=30,
            )
            resp.raise_for_status()
            data = resp.json().get("data", [])

            if not data:  # No more results
                break

            # Yield each analysis individually
            for item in data:
                if debug_limit is not None and total_fetched >= debug_limit:
                    break
                yield AnalysePc(**item)
                total_fetched += 1

            # Break if we get fewer results than requested
            if len(data) < batch_size:
                break

            start += batch_size

        except Exception as e:
            logger.error(f"Error fetching analyses for station {station_code}: {e}")
            break
