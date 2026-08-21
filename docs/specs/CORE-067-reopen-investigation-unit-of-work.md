# CORE-067 — Migrate Reopen Investigation to Unit of Work

## Status

Done

## Context

CORE-057 introduced the application-level `UnitOfWork` abstraction.

CORE-058 introduced `SqliteUnitOfWork`.

CORE-059 migrated `CreateInvestigation` to use `UnitOfWork`.

CORE-060 migrated `AddHypothesis` to use `UnitOfWork`.

CORE-061 migrated `AddEvidence` to use `UnitOfWork`.

CORE-062 migrated `ActivateInvestigation` to use `UnitOfWork`.

CORE-063 migrated `ConfirmHypothesis` to use `UnitOfWork`.

CORE-064 migrated `RejectHypothesis` to use `UnitOfWork`.

CORE-065 migrated `CloseInvestigation` to use `UnitOfWork`.

CORE-066 migrated `RemoveHypothesis` to use `UnitOfWork`.

`ReopenInvestigation` still receives an `InvestigationRepository` and a
`DomainEventRepository` independently.

## Goal

Migrate `ReopenInvestigation` to use `UnitOfWork` as its persistence boundary.

## Acceptance Criteria

- `ReopenInvestigation` receives a `UnitOfWork`.
- Investigations are loaded through `unit_of_work.investigations`.
- Updated investigations are saved through `unit_of_work.investigations`.
- Pending `InvestigationReopened` events are persisted through
  `unit_of_work.domain_events`.
- Successful persistence commits the Unit of Work.
- Persistence failures roll back the Unit of Work.
- Missing investigations still raise `LookupError`.
- Existing domain behavior remains unchanged.

## Architectural Notes

- Transaction coordination remains in the application use case.
- Repository implementations remain behind the `UnitOfWork` abstraction.
- `persist_domain_events()` remains the shared event persistence mechanism.
- Pending events are persisted from the `Investigation` aggregate.
- No other application use case is migrated in this story.
- No Event Bus introduced.
- No Outbox introduced.

## Test Coverage

- Closed investigations can still be reopened.
- Reopened investigations return to `ACTIVE` status.
- Reopening clears `closed_at`.
- `InvestigationReopened` is still persisted.
- Successful execution commits the Unit of Work.
- Persistence failure rolls back the Unit of Work.
- Missing investigations still raise `LookupError`.

## Validation

- pytest — 132 passed
- Ruff — passed
- mypy — 56 source files checked
