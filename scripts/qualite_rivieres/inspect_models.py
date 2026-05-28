# This is a manual check script, not a pytest test module.
# Run with: python scripts/check_qualite_rivieres_models.py

from typing import Any, Dict, Type

import httpx
from pydantic import BaseModel

from hubeau_data.models.qualite_rivieres import (
    AnalysePc,
    ConditionEnvironnementalePc,
    HubeauEnvelope,
    JsonAnalysePc,
    JsonConditionEnvironnementalePc,
    JsonOperationPc,
    JsonStationPc,
    OperationPc,
    StationPc,
)

EndpointDict = Dict[str, tuple[str, Type[HubeauEnvelope[Any]]]]
ENDPOINTS: EndpointDict = {
    "analyse_pc": (
        "https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/analyse_pc",
        JsonAnalysePc,
    ),
    "condition_environnementale_pc": (
        "https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/condition_environnementale_pc",
        JsonConditionEnvironnementalePc,
    ),
    "operation_pc": (
        "https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/operation_pc",
        JsonOperationPc,
    ),
    "station_pc": (
        "https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/station_pc",
        JsonStationPc,
    ),
}

ENDPOINT_SIZES = {
    "operation_pc": 2,  # Trying 1 or 2 for this endpoint to avoid timeout
    # Add more custom sizes for other endpoints if needed
}


def test_endpoint(
    name: str, url: str, model: Type[HubeauEnvelope[Any]], size: int = 5
) -> None:
    print(f"\nTesting endpoint: {name}")
    try:
        response: httpx.Response = httpx.get(url, params={"size": size}, timeout=30)
        response.raise_for_status()
        envelope = model.model_validate_json(response.text)
        print(f"  Success: {envelope.count} records found.")
        if envelope.data:
            first = envelope.data[0]
            geom = getattr(first, "geometry", None)
            print(f"  geometry (first record): {geom}")
    except Exception as e:
        print(f"  ERROR: {e}")


SingleModelDict = Dict[str, tuple[str, Type[BaseModel]]]
SINGLE_MODELS: SingleModelDict = {
    "analyse_pc": (
        "https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/analyse_pc",
        AnalysePc,
    ),
    "condition_environnementale_pc": (
        "https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/condition_environnementale_pc",
        ConditionEnvironnementalePc,
    ),
    "operation_pc": (
        "https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/operation_pc",
        OperationPc,
    ),
    "station_pc": (
        "https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/station_pc",
        StationPc,
    ),
}


def test_single_model(
    name: str, url: str, model: Type[BaseModel], size: int = 1
) -> None:
    print(f"\nTesting single model: {name}")
    try:
        response = httpx.get(url, params={"size": size}, timeout=30)
        response.raise_for_status()
        data = response.json().get("data", [])
        if data:
            instance = model.model_validate(data[0])
            print(f"  Success: {model.__name__} parsed a single record.")
            geom = getattr(instance, "geometry", None)
            print(f"  geometry: {geom}")
        else:
            print("  No data returned.")
    except Exception as e:
        print(f"  ERROR: {e}")


def main() -> None:
    for name, (url, envelope_model) in ENDPOINTS.items():
        test_endpoint(name, url, envelope_model)
    for name, (url, single_model) in SINGLE_MODELS.items():
        test_single_model(name, url, single_model)


if __name__ == "__main__":
    main()
