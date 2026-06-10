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
# → List[ObservationTr] — fully typed Pydantic models
print(observations[0].date_obs, observations[0].resultat_obs)

# Qualité Rivières — water quality stations
stations = client.qualite_rivieres.get_stations(
    params=StationPcParams(code_departement=["75"], size=3)
)
print(stations[0].code_station, stations[0].libelle_station)

# API health check
report = client.hydrometrie.check_health(n_requests=3)
print(report.summary())
# [hydrometrie] checked at 2026-06-10T09:24:07+00:00
#   healthy: 100% (4/4 endpoints)
#   ✓ referentiel/sites      avg=102ms min=68ms max=136ms
#   ✓ observations_tr        avg=376ms min=373ms max=379ms
#   ...

# Data coverage — spot-check a station
cov = client.hydrometrie.data_coverage(code_station="Y120201001")
print(cov.summary())
# [hydrometrie] coverage checked at ...
#   ✓ Y120201001 / observations_tr  count=38156646 latest=2026-06-10T09:15:00Z
#   ✓ Y120201001 / obs_elab         count=271407658 latest=2012-12-01
```

## API Coverage

| API | Status | Notes |
|-----|--------|-------|
| **Hydrométrie** | ✅ Supported | Sites, stations, real-time and elaborated observations. `check_health` and `data_coverage` built-in. |
| **Qualité Rivières** | ⚠️ Partial | Stations and analyses supported. Upstream API has known stability issues — `check_health()` will show it. |
| **Other Hub'Eau APIs** | 📅 Planned | Piezometry, drinking water quality, flow conditions... |

## Features

- Pydantic v2 models for all responses — strict runtime validation, IDE autocomplete
- Typed query `Params` models for every endpoint — no more `**kwargs`
- `check_health(n_requests)` — latency stats per endpoint, healthy ratio
- `data_coverage(code_station, n_stations, random)` — data availability windows
- `HubeauClient` unified entry point + `SimpleHydrometrieClient` for common patterns
- Optional extras: `[dataframe]`, `[geo]`, `[viz]` — install only what you need

## Stack

- Python 3.13+, `mypy --strict`, `ruff`, `uv`, `hatchling`, src-layout
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

## Examples

```zsh
uv run python examples/demo.py
uv run jupyter lab            # open examples/demo.ipynb
```

Exploration and analysis scripts under `scripts/`:

- `scripts/hydrometrie/inspect_fields.py` — inspect raw API fields, generate Pydantic templates
- `scripts/qualite_rivieres/analyze_time_series.py` — time series coverage across stations
- `scripts/qualite_rivieres/check_undocumented_fields.py` — model vs API field diff
- `scripts/qualite_rivieres/inspect_models.py` — validate envelope and geometry models

## Roadmap

- [x] Typed `Params` models for all `hydrometrie` endpoints
- [x] Typed `Params` models for all `qualite_rivieres` endpoints
- [x] `check_health` and `data_coverage` on all implemented APIs
- [x] Optional dependency groups — `pandas`, `geopandas`, `matplotlib` as extras
- [x] `CHANGELOG.md` + `CONTRIBUTING.md`
- [ ] Full Hub'Eau API coverage (piezometry, drinking water, flow conditions...)
- [ ] Async client (`httpx.AsyncClient`)
- [ ] PyPI release

## License

MIT © Pierre Feilles
