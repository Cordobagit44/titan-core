# Contributing to TITAN Core

## Development flow

1. Start from a written specification when domain behavior changes.
2. Add a failing test that expresses the intended behavior.
3. Implement the minimum code required to pass.
4. Refactor while keeping all checks green.
5. Record an ADR only when an architectural decision changes.

## Required checks

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest
```

## Commit format

`<AREA>-<NUMBER>: concise imperative summary`

Example: `CORE-001: Add Investigation aggregate`
