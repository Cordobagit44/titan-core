# CORE-069 — Introduce Application Composition Root

## Status

Done

## Context

TITAN Core already provides:

- application use cases;
- repository abstractions;
- SQLite repository implementations;
- `UnitOfWork`;
- `SqliteUnitOfWork`;
- transaction-safe mutating use cases.

However, there is no composition root that wires application use cases to the
SQLite infrastructure.

## Goal

Introduce an application composition root that constructs a fully wired TITAN
application backed by SQLite.

## Acceptance Criteria

- Introduce `titan.bootstrap`.
- Introduce a `TitanApplication` composition object.
- Introduce a `bootstrap(database)` factory.
- `bootstrap()` creates a `SqliteUnitOfWork`.
- All mutating application use cases share the same Unit of Work.
- Read-only investigation queries use the investigation repository exposed by
  the Unit of Work.
- The composition root exposes all current application use cases.
- SQLite persistence works through the composed application.
- No CLI introduced.
- No web framework introduced.
- No new runtime dependency introduced.

## Architectural Notes

- The composition root belongs outside the domain and application layers.
- Infrastructure knowledge remains outside the application layer.
- Mutating use cases remain dependent on `UnitOfWork`.
- Read-only queries remain dependent on `InvestigationRepository`.
- The same SQLite-backed persistence boundary is shared across the composed
  application.
- No Event Bus introduced.
- No Outbox introduced.

## Test Coverage

- Bootstrap creates a SQLite-backed application.
- Created investigations are persisted through the composed application.
- Investigation activation is persisted.
- Persisted investigations can be retrieved through `GetInvestigation`.
- Persisted investigations can be listed through `ListInvestigations`.
- All current application use cases are exposed by the composition root.

## Validation

- pytest — 135 passed
- Ruff — passed
- mypy — 59 source files checked
