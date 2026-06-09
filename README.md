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

client = HubeauClient()

# Hydrométrie — real-time observations
params = ObservationTrParams(code_station=["Y120201001"], size=3)
observations = client.hydrometrie.get_observations_tr(params=params)
# → List[ObservationTr] — fully typed Pydantic models
print(observations[0].date_obs, observations[0].resultat_obs)

# Qualité Rivières — water quality stations
stations = client.qualite_rivieres.get_stations(libelle_commune="Paris", size=3)
print(stations[0].code_station, stations[0].libelle_station)
```

## API Coverage

| API | Status | Notes |
|-----|--------|-------|
| **Hydrométrie** | ✅ Supported | Sites, stations, real-time and elaborated observations. Typed `Params` models for all endpoints. |
| **Qualité Rivières** | ⚠️ Partial | Works well for targeted queries. The upstream API has known stability issues under load — see `scripts/qualite_rivieres/` for findings. |
| **Other Hub'Eau APIs** | 📅 Planned | |

## Features

- Pydantic v2 models for all responses — strict runtime validation, IDE autocomplete
- Typed query `Params` models for every endpoint — no more `**kwargs`
- `HubeauClient` unified entry point + `SimpleHydrometrieClient` for common patterns
- Ready for pandas / geopandas data science workflows

## Stack

- Python 3.13+, `mypy --strict`, `ruff`, `uv`, `hatchling`, src-layout
- `pytest-httpx` mocked test suite — CI runs without network dependency

## Installation & Development

```zsh
git clone https://github.com/pfei/hubeau-data.git
cd hubeau-data
uv sync
```

```zsh
uv run ruff check .           # lint
uv run mypy .                 # type check
uv run pytest -m "not live"   # fast mocked tests (CI)
uv run pytest -m "live" -s    # real network integration tests
```

## Examples

Notebooks and scripts under `examples/` and `scripts/`. Run instantly with:

```zsh
uv run jupyter lab
```

Exploration scripts by API under `scripts/`:

- `scripts/hydrometrie/` — station and observation exploration
- `scripts/qualite_rivieres/` — API behavior analysis, pagination findings

## Roadmap

- [x] Typed `Params` models for all `hydrometrie` endpoints
- [x] Typed `Params` models for all `qualite_rivieres` endpoints
- [x] Optional dependency groups — `pandas`, `geopandas`, `matplotlib` as extras
- [x] `CHANGELOG.md` + `CONTRIBUTING.md`
- [ ] Rich examples — notebooks and scripts for hydrometrie + qualite_rivieres
- [ ] API health check scripts (responsiveness, uptime, error rate)
- [ ] Full Hub'Eau API coverage (piezometry, drinking water, flow conditions...)
- [ ] Async client (`httpx.AsyncClient`)
- [ ] PyPI release

## License

MIT © Pierre Feilles
