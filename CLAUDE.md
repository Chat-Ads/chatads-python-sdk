# ChatAds Python SDK

Python client for the ChatAds API.

## Package Info

- **Package name**: `chatads-sdk` (on PyPI)
- **Language**: Python 3.9+
- **Type hints**: Yes

## Installation

```bash
pip install chatads-sdk
```

## Usage

See README.md for full usage examples.

## Development

```bash
# Install in development mode
pip install -e .

# Run tests
python -m pytest tests/

# Run smoke tests
python run_sdk_smoke.py
python run_chatads_module_test.py
```

## Publishing

```bash
# Build
python -m build

# Upload to PyPI
twine upload dist/*
```

## Project Structure

- `/chatads_sdk` — Python package source code
- `/tests` — Test files
- `/dist` — Build artifacts (generated)
- `pyproject.toml` — Package configuration (PEP 517/518)
- `README.md` — User-facing documentation
- `run_sdk_smoke.py` — Smoke test script
- `run_chatads_module_test.py` — Module test script

## Related

- `/api` — Backend API this SDK calls
- `/frontend` — Web UI for managing API keys
- `/sdks/chatads-typescript-sdk` — TypeScript equivalent
