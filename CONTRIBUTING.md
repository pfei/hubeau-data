# Contributing

## Setup

```bash
git clone https://github.com/pfei/hubeau-data.git
cd hubeau-data
uv sync --all-extras
```

## Quality checks

Run these before every commit (pre-commit handles this automatically after `uv run pre-commit install`):

```bash
uv run ruff check .          # lint
uv run mypy .                # type check (strict)
uv run pytest -m "not live"  # fast mocked tests
```

To run the full suite including real API calls:

```bash
uv run pytest -m "live" -s
```

## Test markers

- Tests without a marker: mocked, deterministic, run in CI
- `@pytest.mark.live`: real network calls — may be slow or flaky depending on upstream API health

## Commit conventions

This project uses [Conventional Commits](https://www.conventionalcommits.org/):

Examples:

- `feat(hydrometrie): add pagination support for obs_elab`
- `fix(qualite_rivieres): handle empty data response`
- `refactor(models): migrate SiteParams to typed fields`
- `docs: update README quickstart`
- `test: add mocked tests for hydrometrie endpoints`
- `build: add optional dependency groups`

## Adding a new Hub'Eau API

- 1. Add Pydantic response models in `src/hubeau_data/models/<api_name>.py`
- 2. Add typed `Params` models in the same file
- 3. Add the API client in `src/hubeau_data/api/<api_name>.py`
- 4. Register it on `HubeauClient` in `src/hubeau_data/client.py`
- 5. Add mocked + live tests in `tests/test_<api_name>.py`
- 6. Update `README.md` API coverage table
