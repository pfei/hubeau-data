#!/usr/bin/env python3
"""Check the health and data coverage of the Piézométrie API.

Usage:
    uv run python scripts/piezometrie/check_health.py
    uv run python scripts/piezometrie/check_health.py --n-requests 5
    uv run python scripts/piezometrie/check_health.py --bss-id BSS001ABCD
    uv run python scripts/piezometrie/check_health.py --n-stations 5 --random
"""

import argparse

from hubeau_data.client import HubeauClient


def main() -> None:
    parser = argparse.ArgumentParser(description="Piézométrie API health check")
    parser.add_argument(
        "--n-requests",
        type=int,
        default=3,
        help="Number of requests per endpoint (default: 3)",
    )
    parser.add_argument(
        "--bss-id",
        type=str,
        default=None,
        help="BSS station ID for data coverage check",
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
    report = client.piezometrie.check_health(n_requests=args.n_requests)
    print(report.summary())

    print("\n--- Data Coverage ---")
    cov = client.piezometrie.data_coverage(
        bss_id=args.bss_id,
        n_stations=args.n_stations,
        random=args.random,
    )
    print(cov.summary())


if __name__ == "__main__":
    main()
