import sys
from typing import Any

import httpx
from pydantic import BaseModel


def fetch_sample(url: str, n: int = 10, **params: Any) -> list[dict[str, Any]]:
    params["size"] = n
    resp = httpx.get(url, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json().get("data", [])
    if not isinstance(data, list):
        return []
    return data


def get_model_fields(model: type[BaseModel]) -> set[str]:
    return set(model.model_fields.keys())


def check_undocumented_fields(
    url: str, model: type[BaseModel], n: int = 10, **params: Any
) -> None:
    print(f"Fetching {n} samples from {url} ...")
    data = fetch_sample(url, n=n, **params)
    if not data:
        print("No data returned!")
        return

    response_keys: set[str] = set()
    for item in data:
        response_keys.update(item.keys())

    model_fields: set[str] = get_model_fields(model)
    extra_fields = response_keys - model_fields
    missing_fields = model_fields - response_keys

    print("\nFields in API response but NOT in model:")
    for f in sorted(extra_fields):
        print(f"  - {f}")

    print("\nFields in model but NOT in API response (may be OK if optional):")
    for f in sorted(missing_fields):
        print(f"  - {f}")

    print("\nAll fields in API response:")
    for f in sorted(response_keys):
        print(f"  - {f}")

    print("\nAll fields in model:")
    for f in sorted(model_fields):
        print(f"  - {f}")


if __name__ == "__main__":
    from hubeau_data.models.qualite_rivieres import (
        AnalysePc,
        ConditionEnvironnementalePc,
        OperationPc,
        StationPc,
    )

    endpoints: dict[str, tuple[str, type[BaseModel]]] = {
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

    if len(sys.argv) < 2 or sys.argv[1] not in endpoints:
        print(
            "Usage:\n"
            "  poetry run python scripts/check_undocumented_fields.py "
            "[analyse_pc|condition_environnementale_pc]"
        )
        sys.exit(1)

    endpoint_name = sys.argv[1]
    url, model = endpoints[endpoint_name]
    check_undocumented_fields(url, model, n=20)
