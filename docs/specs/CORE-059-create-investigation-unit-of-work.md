# CORE-059 — Migrate Create Investigation to Unit of Work

## Status

Done

## Context

CORE-057 introduced the application-level `UnitOfWork` abstraction.

CORE-058 introduced `SqliteUnitOfWork`, allowing investigation persistence and
domain event persistence to participate in one SQLite transaction.

`CreateInvestigation` still receives an `InvestigationRepository` and a
`DomainEventRepository` independently and therefore does not control the
transaction through a Unit of Work.

## Goal

Migrate `CreateInvestigation` to use `UnitOfWork` as its persistence boundary.

## Acceptance Criteria

- `CreateInvestigation` receives a `UnitOfWork`.
- The investigation is saved through `unit_of_work.investigations`.
- Pending domain events are persisted through `unit_of_work.domain_events`.
- The Unit of Work is committed after successful persistence.
- The Unit of Work is rolled back if persistence fails.
- The created investigation is still returned.
- Existing domain behavior remains unchanged.

## Architectural Notes

- Transaction coordination remains in the application use case.
- Repository implementations remain behind the Unit of Work abstraction.
- `persist_domain_events()` remains the shared event persistence mechanism.
- No other application use case is migrated in this story.
- No Event Bus introduced.
- No Outbox introduced.

## Test Coverage

- Investigation creation still returns and persists the aggregate.
- `InvestigationCreated` is still persisted.
- Successful execution commits the Unit of Work.
- Persistence failure rolls back the Unit of Work.

## Validation

- pytest — 116 passed
- Ruff — passed
- mypy — 56 source files checked
