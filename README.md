> ⚠️ **Pre-Alpha Notice**
>
> This project is in a **very early, pre-alpha state**.\
> The goal is to become a solid, typed, and reference Python client for the Hubeau APIs.
> Expect rapid changes, breaking updates, and incomplete coverage.
> Contributions, feedback, and issue reports are very welcome!

# hubeau-data

Pythonic, typed, and modern client for the Hubeau water data APIs.

## API Coverage and Status

| API Name | Status | Notes |
| --------------------- | ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Qualité Rivières** | ⚠️ Limited Support | Initial implementation with known limitations. API has pagination issues and high error rates (~60%) when querying large datasets. Best used for targeted queries rather than bulk data extraction. |
| **Hydrométrie** | ✅ Supported | Full access to sites, stations, and real-time or elaborated observations. Implemented via unified and simple client layers. |
| **Other Hubeau APIs** | 📅 Planned | Will be added in future releases. |

> **Note on Qualité Rivières API:** > Our exploration revealed significant rate limiting and stability issues when attempting exhaustive data extraction. The API works well for targeted queries but may not be suitable for comprehensive data analysis across all stations. See the `scripts/qualite_rivieres/` directory for exploration tools and findings.

## Features

- Typed, Pythonic client for the Hubeau water data APIs
- Easy querying of water quality, hydrometry observations, and station data
- Returns results as Pydantic v2 models for strict runtime type safety
- Ready for use in data science workflows with production-ready `pandas` and `geopandas` DataFrames

## Development Model

- Modern Python (**3.13+**)
- Strict typing throughout the codebase (`mypy --strict`)
- Enforced linting and formatting via fast Rust-powered tooling (`ruff`)
- Standardized package architecture adhering to the [src-layout](https://realpython.com/python-application-layouts/)
- Built using **`hatchling`** as the PEP 517 build backend and **`uv`** for dependency management

## Quickstart

```python
from hubeau_data.client import HubeauClient

client = HubeauClient()

# 1. Qualité Rivières Endpoint
stations = client.qualite_rivieres.get_stations(libelle_commune="Paris", size=3)
print(stations)

# 2. Hydrométrie Endpoint
observations = client.hydrometrie.get_observations_tr(code_station="Y120201001", size=3)
print(observations)
```

## Example Notebooks

Continuously updated example notebooks and dashboards are available under the `examples/` directory.

You can run them locally using Jupyter Lab or Notebook instantly through `uv`:

```zsh
uv run jupyter lab
```

## Installation & Development

This project leverages [uv](https://github.com/astral-sh/uv) for fast, modern dependency and workspace orchestration.

### 1. Project Setup

Clone the repository and synchronize the environment. `uv` will automatically
provision Python 3.13, create a virtual environment, and install the package along with its development groups:

```zsh
git clone https://github.com/your-username/hubeau-data.git
cd hubeau-data
uv sync
```

### 2. Quality Assurance Commands

Run the full local verification suite through `uv run`:

- **Linting & Formatting:**
  ```zsh
  uv run ruff check .
  ```
- **Type Checking (Strict Mode):**
  ```zsh
  uv run mypy .
  ```
- **Run Fast Mocked Test Suite:**
  ```zsh
  uv run pytest -m "not live"
  ```
- **Run Real Network Integration Tests:**
  ```zsh
  uv run pytest -m "live" -s
  ```

## How Imports Work

This project uses the modern Python **src-layout** combined with a PEP 517 build system powered by `hatchling`.

When you run `uv sync`, the project is automatically installed in **editable mode** (the standard PEP 660 equivalent of `pip install -e .`) inside the `.venv` directory. An optimized import hook proxy is placed in the virtual environment's `site-packages`, routing any package calls straight to your local `src/hubeau_data` directory.

This allows you to safely use absolute imports across any test, script, or notebook without manual path manipulations:

```python
from hubeau_data.client import HubeauClient
```

Always prefix your execution commands with `uv run` (e.g., `uv run pytest`, `uv run demo.py`) to ensure Python looks up the package matching your isolated workspace environment. Alternatively, you can activate the virtual environment manually within your shell:

```zsh
source .venv/bin/activate
```

## Inspect Scripts

Scripts for exploring and inspecting the Hubeau APIs are organized by endpoint under the `scripts/` directory. For example:

- **qualite_rivieres/**: Tools for the "Qualité Rivières" API.
  - `explore.py`: Interactive exploration of the API.
  - `analyze_time_series.py`: Paginated fetching and analysis across stations with built-in API error fallback.

**Usage:**

```zsh
uv run python scripts/qualite_rivieres/explore.py
```

## License

MIT License © Pierre Feilles
