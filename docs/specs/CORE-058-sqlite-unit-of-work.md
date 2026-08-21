# CORE-058 — Implement SQLite Unit of Work

## Status

Done

## Context

CORE-057 introduced the application-level `UnitOfWork` abstraction.

The SQLite investigation repository and SQLite domain event repository currently
create and manage independent SQLite connections.

Both repositories also commit their own write operations, preventing
investigation state and corresponding domain events from participating in one
application-controlled transaction.

## Goal

Implement a SQLite Unit of Work that coordinates investigation persistence and
domain event persistence through one shared SQLite connection and one explicit
transaction boundary.

## Acceptance Criteria

- Introduce `SqliteUnitOfWork`.
- `SqliteUnitOfWork` implements `UnitOfWork`.
- The Unit of Work exposes a `SqliteInvestigationRepository`.
- The Unit of Work exposes a `SqliteDomainEventRepository`.
- Both repositories use the same SQLite connection when managed by the Unit of
  Work.
- `commit()` commits changes made through both repositories.
- `rollback()` rolls back changes made through both repositories.
- Standalone SQLite repositories preserve their existing behavior.
- Existing tests remain green.

## Architectural Notes

- Transaction coordination belongs to SQLite infrastructure.
- The application-level `UnitOfWork` abstraction remains unchanged.
- Repositories may use an externally managed SQLite connection.
- Repositories must not independently commit writes when their connection is
  managed by a Unit of Work.
- Existing standalone repository behavior must remain backward compatible.
- No application use case is migrated to Unit of Work in this story.
- No Event Bus introduced.
- No Outbox introduced.

## Out of Scope

This story does not:

- refactor application use cases to receive `UnitOfWork`;
- change domain behavior;
- change domain event definitions;
- introduce an Event Bus;
- introduce an Outbox;
- introduce nested transactions;
- introduce distributed transactions.

## Definition of Done

- RED → GREEN → REFACTOR
- SQLite Unit of Work covered by integration tests
- Commit behavior verified
- Rollback behavior verified
- Existing standalone repository tests remain green
- Full pytest suite passes
- Ruff passes
- mypy passes
