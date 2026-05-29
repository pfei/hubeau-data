#!/usr/bin/env python3
"""Demo script showcasing the hubeau-data client library functionality.

This script provides a terminal-focused execution
to validate the environment and see the client in action.
"""

import sys

from httpx import ReadTimeout

from hubeau_data.client import HubeauClient


def run_demo() -> None:
    print("=" * 60)
    print("  HUBEAU-DATA CLIENT LIBRARY DEMO  ".center(60, "="))
    print("=" * 60)

    # Initialize the unified client
    print("\n[1/3] Initializing HubeauClient...")
    client = HubeauClient()
    print("✓ Client initialized successfully.")

    # --- Qualité Rivières Demo ---
    print("\n[2/3] Querying 'Qualité Rivières' API...")
    try:
        # Fetching stations in Paris (75) area
        stations_qr = client.qualite_rivieres.get_stations(
            code_departement="75", size=3
        )

        print(f"✓ Found {len(stations_qr)} stations in Paris area.")
        for i, station in enumerate(stations_qr, 1):
            print(
                f"  -> Station #{i}: {station.code_station} - {station.libelle_station}"
            )
            print(
                f"     Location: {station.libelle_commune} ({station.code_commune}) | "
                f"URI: {station.uri_station}"
            )

    except ReadTimeout:
        print(
            "⚠️  Note: 'Qualité Rivières' API timed out. This upstream API has known "
            "stability and performance limitations under heavy load.",
            file=sys.stderr,
        )
    except Exception as e:
        print(f"❌ Error querying Qualité Rivières API: {e}", file=sys.stderr)

    # --- Hydrométrie Demo ---
    print("\n[3/3] Querying 'Hydrométrie' API...")
    try:
        # Example station code (frequent reference station)
        target_station = "Y120201001"
        print(f"Fetching real-time observations for station: {target_station}")

        observations = client.hydrometrie.get_observations_tr(
            code_station=target_station, size=3
        )

        print(f"✓ Retrieved {len(observations)} real-time observations.")
        for i, obs in enumerate(observations, 1):
            print(
                f"  -> Obs #{i}: Date: {obs.date_obs} | "
                f"Value: {obs.resultat_obs} {obs.grandeur_hydro}"
            )

    except Exception as e:
        print(f"❌ Error querying Hydrométrie API: {e}", file=sys.stderr)

    print("\n" + "=" * 60)
    print("  DEMO COMPLETED SUCCESSFULLY  ".center(60, "="))
    print("=" * 60)


if __name__ == "__main__":
    run_demo()
