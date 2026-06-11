#!/usr/bin/env python3
"""Check the health and data coverage of the Qualité Eau Potable API.

Usage:
    uv run python scripts/eau_potable/check_health.py
    uv run python scripts/eau_potable/check_health.py --n-requests 5
    uv run python scripts/eau_potable/check_health.py --commune 75056
    uv run python scripts/eau_potable/check_health.py --n-communes 5 --random
"""

import argparse

from hubeau_data.client import HubeauClient


def main() -> None:
    parser = argparse.ArgumentParser(description="Eau Potable API health check")
    parser.add_argument(
        "--n-requests",
        type=int,
        default=3,
        help="Number of requests per endpoint (default: 3)",
    )
    parser.add_argument(
        "--commune",
        type=str,
        default=None,
        help="Commune INSEE code for data coverage check",
    )
    parser.add_argument(
        "--n-communes",
        type=int,
        default=3,
        help="Number of communes for data coverage sample (default: 3)",
    )
    parser.add_argument(
        "--random",
        action="store_true",
        help="Sample communes randomly instead of first N",
    )
    args = parser.parse_args()

    client = HubeauClient()

    print("--- Health Check ---")
    report = client.eau_potable.check_health(n_requests=args.n_requests)
    print(report.summary())

    print("\n--- Data Coverage ---")
    cov = client.eau_potable.data_coverage(
        code_commune=args.commune,
        n_communes=args.n_communes,
        random=args.random,
    )
    print(cov.summary())


if __name__ == "__main__":
    main()
