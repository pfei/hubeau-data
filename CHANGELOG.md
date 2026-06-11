# Changelog

All notable changes to this project will be documented in this file.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added

- Full Hub'Eau API coverage — 11 APIs implemented:
  `hydrometrie`, `qualite_rivieres`, `piezometrie`, `qualite_nappes`,
  `ecoulement`, `temperature`, `prelevements`, `hydrobiologie`,
  `poisson`, `eau_potable`, `phytopharmaceutiques`
- `check_health(n_requests)` on every API — latency stats, healthy ratio
- `data_coverage(...)` on every API — data availability windows
- CLI health check scripts for every API under `scripts/<api>/check_health.py`
- Typed `Params` models for every endpoint across all APIs
- Pydantic v2 models for all API responses
- Pydantic mypy plugin for strict type checking
- Mocked test suite using `pytest-httpx` — CI runs without network dependency
- `@pytest.mark.live` marker to separate integration from unit tests
- `xfail` markers on known unstable endpoints (qualite_rivieres, qualite_nappes,
  temperature chronique, prelevements chroniques)
- `models/health.py` — shared `EndpointStatus`, `HealthReport`, `DataWindow`,
  `CoverageReport` models
- Optional dependency groups: `[dataframe]`, `[geo]`, `[viz]`, `[all]`
- `CHANGELOG.md` + `CONTRIBUTING.md`
- CI badge in README

### Changed

- Migrated all API methods from `**kwargs` to typed `Params` models
- Rewrote README: full API coverage table, assertive tone, accurate quickstart
- Split runtime dependencies — core install requires only `httpx` and `pydantic`
- Pinned `mypy<2.0` pending pydantic plugin compatibility with mypy 2.x
- Removed `SimpleHydrometrieClient` — `HubeauClient` is the single entry point

### Fixed

- `get_obs_elab` was outside `HydrometrieAPI` class (indentation bug)
- `code_entite` → `code_station` for hydrometrie observations (API mismatch)
- `Station` and `Site` fields relaxed to `Optional` — Hub'Eau returns null on many fields
- `phytopharmaceutiques` BASE_URL corrected to `/api/v1/vente_achat_phyto`

### Skipped

- **Surveillance Littoral** — API being decommissioned by Hub'Eau
- **Indicateurs Services** — API under maintenance
