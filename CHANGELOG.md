# Changelog

All notable changes to this project will be documented in this file.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added

- Typed `Params` models for all endpoints: `SiteParams`, `StationParams`,
  `ObservationTrParams`, `ObsElabParams`, `StationPcParams`, `AnalysePcParams`
- Pydantic mypy plugin for strict type checking across all Params models
- Mocked test suite (10 tests) using `pytest-httpx` — CI runs without network
- `@pytest.mark.live` marker to separate integration tests from unit tests
- `xfail` marker on unstable Qualité Rivières live test (known upstream issue)
- CI badge in README

### Changed

- Migrated all API methods from `**kwargs` to typed `Params` models
- Fixed `get_obs_elab` indentation bug (method was outside `HydrometrieAPI` class)
- Rewrote README: assertive tone, accurate quickstart, roadmap section
- Split runtime dependencies into optional extras: `[dataframe]`, `[geo]`, `[viz]`, `[all]`
- Core install now only requires `httpx` and `pydantic`
- Pinned `mypy<2.0` pending pydantic plugin compatibility with mypy 2.x
