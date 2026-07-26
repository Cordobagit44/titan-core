# CORE-029: SQLite Investigation Repository

## User Story

As the application,
I want an SQLite implementation of the investigation repository,
so that investigations can be persisted beyond process lifetime.

## Acceptance Criteria

- A `SqliteInvestigationRepository` exists.
- It implements `InvestigationRepository`.
- It persists investigations using the standard `sqlite3` module.
- It supports:
  - `save()`
  - `get()`
  - `list()`
- Existing application use cases work without modification.
- Existing behavior remains unchanged.
