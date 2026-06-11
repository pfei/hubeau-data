#!/usr/bin/env python3
"""Check the health and data coverage of the Poisson API.

Usage:
    uv run python scripts/poisson/check_health.py
    uv run python scripts/poisson/check_health.py --n-requests 5
    uv run python scripts/poisson/check_health.py --station 01000001
    uv run python scripts/poisson/check_health.py --n-stations 5 --random
"""

import argparse

from hubeau_data.client import HubeauClient


def main() -> None:
    parser = argparse.ArgumentParser(description="Poisson API health check")
    parser.add_argument(
        "--n-requests",
        type=int,
        default=3,
        help="Number of requests per endpoint (default: 3)",
    )
    parser.add_argument(
        "--station", type=str, default=None, help="Station code for data coverage check"
    )
    parser.add_argument(
        "--n-stations",
        type=int,
        default=3,
        help="Number of stations for data coverage sample (default: 3)",
    )
    parser.add_argument(
        "--random",
        action="store_true",
        help="Sample stations randomly instead of first N",
    )
    args = parser.parse_args()

    client = HubeauClient()

    print("--- Health Check ---")
    report = client.poisson.check_health(n_requests=args.n_requests)
    print(report.summary())

    print("\n--- Data Coverage ---")
    cov = client.poisson.data_coverage(
        code_station=args.station,
        n_stations=args.n_stations,
        random=args.random,
    )
    print(cov.summary())


if __name__ == "__main__":
    main()
