# Changelog

All notable changes to this project will be documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [0.2.0] - 2026-06-15

### Changed — Breaking

- **All `get_*` methods now return `PagedResponse[T]` instead of `List[T]`.**
  `PagedResponse` exposes three fields:

  - `data: list[T]` — the records for this page
  - `count: int` — total records available server-side
  - `next_cursor: str | None` — pass as `cursor=` (or `page=`) param to fetch the next page

  Migration: replace `result[0]` with `result.data[0]`, `len(result)` with `len(result.data)`,
  and `for item in result` with `for item in result.data`.

- **`hydrometrie` `ObservationTrParams` and `ObsElabParams`**: `code_station`/`code_site`
  replaced by `code_entite` (fix carried over from 0.1.0 — see below).

- **`qualite_nappes` and `qualite_rivieres`**: removed the ad-hoc `max_records`/`page`
  loop in `get_analyses()`. Pagination is now handled uniformly via `next_cursor`.

### Added

- `PagedResponse[T]` generic Pydantic model (`hubeau_data.models.pagination`).
- `extract_next_cursor(next_url)` utility function (`hubeau_data.utils`) — detects
  cursor-based and page-based pagination from Hub'Eau `next` URLs.

### Fixed

- `hydrometrie` `ObservationTrParams`/`ObsElabParams`: the correct Hub'Eau query
  parameter is `code_entite`, not `code_station` or `code_site`. The previous names
  were silently ignored by the API, returning unfiltered global results.
  Audited `qualite_rivieres`, `ecoulement`, `poisson`, `temperature` — all correctly
  use `code_station` for their respective endpoints, no changes needed.

## [0.1.0] - 2026-06-13

### Fixed

- **Breaking**: `hydrometrie` real-time and elaborated observations endpoints
  (`observations_tr`, `obs_elab`) only support the `code_entite` query
  parameter, not `code_station` or `code_site` as previously modeled.
  Those invalid parameters were silently ignored by the Hub'Eau API,
  causing `get_observations_tr()`, `get_obs_elab()`, and
  `data_coverage()` to return globally unfiltered results instead of
  data for the requested station.

  `ObservationTrParams` and `ObsElabParams` now expose a single
  `code_entite: Optional[List[str]]` field, accepting either a site or
  station code. Callers passing `code_station=` or `code_site=` to
  these two params models must switch to `code_entite=`.

  Audited the equivalent `data_coverage()` pattern across
  `qualite_rivieres`, `ecoulement`, `poisson`, and `temperature` — all
  four correctly use `code_station` for their respective endpoints, no
  changes needed there. A full audit of query parameters across the
  remaining APIs is tracked as future work.

## [0.0.1] - 2026-06-12

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
