# CORE-062 — Migrate Activate Investigation to Unit of Work

## Status

Done

## Context

CORE-057 introduced the application-level `UnitOfWork` abstraction.

CORE-058 introduced `SqliteUnitOfWork`.

CORE-059 migrated `CreateInvestigation` to use `UnitOfWork`.

CORE-060 migrated `AddHypothesis` to use `UnitOfWork`.

CORE-061 migrated `AddEvidence` to use `UnitOfWork`.

`ActivateInvestigation` still receives an `InvestigationRepository` and a
`DomainEventRepository` independently.

## Goal

Migrate `ActivateInvestigation` to use `UnitOfWork` as its persistence boundary.

## Acceptance Criteria

- `ActivateInvestigation` receives a `UnitOfWork`.
- Investigations are loaded through `unit_of_work.investigations`.
- Updated investigations are saved through `unit_of_work.investigations`.
- Pending `InvestigationActivated` events are persisted through
  `unit_of_work.domain_events`.
- Successful persistence commits the Unit of Work.
- Persistence failures roll back the Unit of Work.
- Missing investigations still raise `LookupError`.
- Existing domain behavior remains unchanged.

## Architectural Notes

- Transaction coordination remains in the application use case.
- Repository implementations remain behind the `UnitOfWork` abstraction.
- `persist_domain_events()` remains the shared event persistence mechanism.
- No other application use case is migrated in this story.
- No Event Bus introduced.
- No Outbox introduced.

## Test Coverage

- Activation still returns the investigation.
- Investigation status still becomes active.
- `InvestigationActivated` is still persisted.
- Successful execution commits the Unit of Work.
- Persistence failure rolls back the Unit of Work.
- Missing investigations still raise `LookupError`.

## Validation

- pytest — 122 passed
- Ruff — passed
- mypy — 56 source files checked
