#!/usr/bin/env python3
"""Check the health and data coverage of the Phytopharmaceutiques API.

Usage:
    uv run python scripts/phytopharmaceutiques/check_health.py
    uv run python scripts/phytopharmaceutiques/check_health.py --n-requests 5
"""

import argparse

from hubeau_data.client import HubeauClient


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Phytopharmaceutiques API health check"
    )
    parser.add_argument(
        "--n-requests",
        type=int,
        default=3,
        help="Number of requests per endpoint (default: 3)",
    )
    args = parser.parse_args()

    client = HubeauClient()

    print("--- Health Check ---")
    report = client.phytopharmaceutiques.check_health(n_requests=args.n_requests)
    print(report.summary())

    print("\n--- Data Coverage ---")
    cov = client.phytopharmaceutiques.data_coverage()
    print(cov.summary())


if __name__ == "__main__":
    main()
