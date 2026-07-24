# TITAN Core

> Evidence. Reasoning. Confidence.

TITAN Core is the domain foundation of a platform for traceable investigations. Its purpose is to preserve the reasoning chain from original evidence to an assessment without coupling the domain to databases, APIs, interfaces, or AI vendors.

## Status

**Genesis — CORE-000 Bootstrap**

No business behavior is implemented yet. The repository establishes the development environment and architectural boundary for `CORE-001: Investigation`.

## Requirements

- Python 3.13
- [uv](https://docs.astral.sh/uv/)

## Getting started

```bash
uv sync
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest
```

Install Git hooks:

```bash
uv run pre-commit install
```

## Core rule

Code under `src/titan/core` may depend only on the Python standard library and other modules inside TITAN Core.

## License

MIT
