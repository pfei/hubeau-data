# hubeau-data

[![CI](https://github.com/pfei/hubeau-data/actions/workflows/ci.yml/badge.svg)](https://github.com/pfei/hubeau-data/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/)
[![Checked with mypy](https://img.shields.io/badge/mypy-strict-green.svg)](https://mypy.readthedocs.io/en/stable/config_file.html#using-a-pyproject-toml-file)
[![Linting: ruff](https://img.shields.io/badge/linting-ruff-orange.svg)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Package Manager: uv](https://img.shields.io/badge/managed%20by-uv-purple.svg)](https://github.com/astral-sh/uv)

Typed, modern Python client for the [Hub'Eau](https://hubeau.eaufrance.fr/) water data APIs.

Hub'Eau exposes 15+ REST APIs for French national water data — but no official typed Python client exists.
This library fills that gap: Pydantic v2 models, strict typing, and a clean interface ready for data science workflows.

## Quickstart

```python
from hubeau_data.client import HubeauClient
from hubeau_data.models.hydrometrie import ObservationTrParams
from hubeau_data.models.qualite_rivieres import StationPcParams

client = HubeauClient()

# Hydrométrie — real-time observations
params = ObservationTrParams(code_station=["Y120201001"], size=3)
observations = client.hydrometrie.get_observations_tr(params=params)
print(observations[0].date_obs, observations[0].resultat_obs)

# Qualité Rivières — water quality stations
stations = client.qualite_rivieres.get_stations(
    params=StationPcParams(code_departement=["75"], size=3)
)
print(stations[0].code_station, stations[0].libelle_station)

# Eau potable — drinking water analyses for a commune
from hubeau_data.models.eau_potable import ResultatEauPotableParams
resultats = client.eau_potable.get_resultats_dis(
    params=ResultatEauPotableParams(code_commune=["75056"], size=5)
)
print(resultats[0].libelle_parametre, resultats[0].resultat_numerique)

# Phytopharmaceutiques — national pesticide sales
from hubeau_data.models.phytopharmaceutiques import VenteSubstanceParams
ventes = client.phytopharmaceutiques.get_ventes_substances(
    params=VenteSubstanceParams(type_territoire="National", size=5)
)
print(ventes[0].libelle_substance, ventes[0].quantite, ventes[0].annee)

# API health check — works on every API
report = client.hydrometrie.check_health(n_requests=3)
print(report.summary())

# Data coverage — spot-check stations
cov = client.hydrometrie.data_coverage(code_station="Y120201001")
print(cov.summary())
```

## Async client

For bulk data collection — e.g. fetching many stations before inserting into a database —
`AsyncHubeauClient` mirrors the sync client and supports `asyncio.gather()` for parallel requests:

```python
import asyncio
from hubeau_data.async_client import AsyncHubeauClient
from hubeau_data.models.hydrometrie import ObservationTrParams

async def main():
    async with AsyncHubeauClient() as client:
        codes = ["Y120201001", "K418001001", "A1234567"]
        tasks = [
            client.hydrometrie.get_observations_tr(
                params=ObservationTrParams(code_station=[c], size=10)
            )
            for c in codes
        ]
        results = await asyncio.gather(*tasks)
        for code, obs in zip(codes, results):
            print(code, len(obs), "observations")

asyncio.run(main())
```

All 11 APIs are available on `AsyncHubeauClient` with the same method names as the sync client
(`get_sites`, `get_stations`, etc.) — just `await` them. Retry logic (tenacity) applies to async
requests too. `check_health` and `data_coverage` are sync-only (diagnostic tools, not bulk operations).

## API Coverage

| API | Status | Notes |
|-----|--------|-------|
| **Hydrométrie** | ✅ Supported | Sites, stations, real-time and elaborated observations |
| **Qualité des cours d'eau** | ⚠️ Partial | Stations and analyses. Upstream API has known stability issues |
| **Piézométrie** | ✅ Supported | Stations, chroniques, chroniques temps réel |
| **Qualité des nappes** | ⚠️ Partial | Stations and analyses. Known 503/timeout issues |
| **Écoulement** | ✅ Supported | Stations, observations, campaigns |
| **Température** | ✅ Supported | Stations and chroniques |
| **Prélèvements en eau** | ✅ Supported | Ouvrages, points de prélèvement, chroniques |
| **Hydrobiologie** | ✅ Supported | Stations, indices (IBGN/IBMR/IBD/IPR), taxons |
| **Poisson** | ✅ Supported | Stations, indicateurs IPR/IPR+, observations, operations |
| **Qualité eau potable** | ✅ Supported | Communes/UDI links, analysis results |
| **Phytopharmaceutiques** | ✅ Supported | Purchases and sales by substance and product |
| **Surveillance Littoral** | 🚫 Skipped | API being decommissioned by Hub'Eau |
| **Indicateurs Services** | 🚧 Maintenance | API under maintenance — see services.eaufrance.fr |

All supported APIs expose `check_health(n_requests)` and `data_coverage(...)`, and are available
on both `HubeauClient` (sync) and `AsyncHubeauClient` (async, except health/coverage).

## Features

- Pydantic v2 models for all responses — strict runtime validation, IDE autocomplete
- Typed query `Params` models for every endpoint — no more `**kwargs`
- Sync (`HubeauClient`) and async (`AsyncHubeauClient`) clients, same method names
- Automatic retry with exponential backoff (tenacity) on transient errors — Hub'Eau APIs have known stability issues
- `check_health(n_requests)` — latency stats per endpoint, healthy ratio
- `data_coverage(...)` — data availability windows per station or territory
- Optional extras: `[dataframe]`, `[geo]`, `[viz]` — install only what you need

## Stack

- Python 3.13+, `mypy --strict`, `ruff`, `uv`, `hatchling`, src-layout
- `httpx` + `tenacity` for resilient sync/async HTTP
- `pytest-httpx` mocked test suite — CI runs without network dependency

## Installation & Development

```zsh
git clone https://github.com/pfei/hubeau-data.git
cd hubeau-data
uv sync                   # core only
uv sync --all-extras      # with pandas, geopandas, matplotlib
```

```zsh
uv run ruff check .           # lint
uv run mypy .                 # type check
uv run pytest -m "not live"   # fast mocked tests (CI)
uv run pytest -m "live" -s    # real network integration tests
```

## Examples & Scripts

```zsh
uv run python examples/demo.py
uv run jupyter lab            # open examples/demo.ipynb
```

Health check scripts for every API under `scripts/<api>/check_health.py`:

```zsh
uv run python scripts/hydrometrie/check_health.py --n-requests 3 --random
uv run python scripts/qualite_rivieres/check_health.py --n-requests 2
uv run python scripts/eau_potable/check_health.py --commune 75056
uv run python scripts/phytopharmaceutiques/check_health.py
```

Exploration scripts under `scripts/qualite_rivieres/` and `scripts/hydrometrie/`.

## Roadmap

- [x] Full Hub'Eau API coverage (11 APIs implemented)
- [x] `check_health` and `data_coverage` on all APIs
- [x] Typed `Params` models for every endpoint
- [x] Automatic retry with exponential backoff (tenacity)
- [x] Async client (`AsyncHubeauClient`, all 11 APIs)
- [x] Optional dependency groups — `pandas`, `geopandas`, `matplotlib` as extras
- [x] `CHANGELOG.md` + `CONTRIBUTING.md`
- [ ] PyPI release

## License

MIT © Pierre Feilles
