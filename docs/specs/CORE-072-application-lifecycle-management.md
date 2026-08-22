# CORE-072 — Add Application Lifecycle Management

## Status

Done

## Context

`SqliteUnitOfWork` owns a SQLite connection used by both the investigation and
domain event repositories.

Until this story, the Unit of Work exposed `commit()` and `rollback()` but had
no explicit lifecycle operation for releasing the SQLite connection.

The application composition root also exposed no application-level shutdown
mechanism, leaving the connection lifetime implicit.

## Goal

Add explicit lifecycle management so SQLite resources can be released
deterministically by both the Unit of Work and the composed application.

## Acceptance Criteria

- `SqliteUnitOfWork` exposes `close()`.
- `close()` releases the underlying SQLite connection.
- Operations attempted through repositories after close fail because the
  database connection is closed.
- `TitanApplication` exposes `close()`.
- `TitanApplication.close()` releases the SQLite resources owned by the
  application.
- Existing application use cases remain unchanged.
- Existing transaction behavior remains unchanged.
- No context manager support is introduced in this story.
- No CLI or web framework lifecycle integration is introduced.

## Architectural Notes

- Resource ownership remains in the infrastructure/composition boundary.
- Application use cases remain unaware of connection lifecycle details.
- `TitanApplication` delegates shutdown to the SQLite Unit of Work created by
  the composition root.
- Explicit close semantics are preferred over relying on process shutdown or
  garbage collection.
- Context manager support may be introduced separately if needed.

## Test Coverage

- `SqliteUnitOfWork.close()` closes the SQLite connection.
- Repository access after Unit of Work close raises `sqlite3.ProgrammingError`.
- `TitanApplication.close()` releases the underlying SQLite resources.
- Application queries after close fail because the database connection is
  closed.
- Existing bootstrap wiring remains functional.

## Validation

- pytest — 138 passed
- Ruff — passed
- mypy — 60 source files checked
