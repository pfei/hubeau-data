#!/usr/bin/env python3
"""Check the health and data coverage of the Prélèvements en eau API.

Usage:
    uv run python scripts/prelevements/check_health.py
    uv run python scripts/prelevements/check_health.py --n-requests 5
    uv run python scripts/prelevements/check_health.py --ouvrage OPR0000000001
    uv run python scripts/prelevements/check_health.py --n-ouvrages 5 --random
"""

import argparse

from hubeau_data.client import HubeauClient


def main() -> None:
    parser = argparse.ArgumentParser(description="Prélèvements en eau API health check")
    parser.add_argument(
        "--n-requests",
        type=int,
        default=3,
        help="Number of requests per endpoint (default: 3)",
    )
    parser.add_argument(
        "--ouvrage", type=str, default=None, help="Ouvrage code for data coverage check"
    )
    parser.add_argument(
        "--n-ouvrages",
        type=int,
        default=3,
        help="Number of ouvrages for data coverage sample (default: 3)",
    )
    parser.add_argument(
        "--random",
        action="store_true",
        help="Sample ouvrages randomly instead of first N",
    )
    args = parser.parse_args()

    client = HubeauClient()

    print("--- Health Check ---")
    report = client.prelevements.check_health(n_requests=args.n_requests)
    print(report.summary())

    print("\n--- Data Coverage ---")
    cov = client.prelevements.data_coverage(
        code_ouvrage=args.ouvrage,
        n_ouvrages=args.n_ouvrages,
        random=args.random,
    )
    print(cov.summary())


if __name__ == "__main__":
    main()
