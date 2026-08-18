# CORE-047 — Persist Reopened Investigation Domain Event

## User Story

As the application,
I want domain events produced during investigation reopening to be persisted,
so that the reopening of an investigation is durably recorded after the use case completes.

## Acceptance Criteria

- `ReopenInvestigation` receives an `InvestigationRepository`.
- `ReopenInvestigation` also receives a `DomainEventRepository`.
- Reopening an investigation still loads the investigation by identifier.
- A missing investigation still raises `LookupError`.
- Reopening the investigation still changes its domain state to `ACTIVE`.
- Reopening the investigation still clears `closed_at`.
- The investigation is still saved after reopening.
- The `InvestigationReopened` event produced by the aggregate is persisted.
- The reopened investigation is still returned.
- Existing domain behavior remains unchanged.
- Existing persistence abstractions remain unchanged.

## Technical Notes

- Reuse the existing `persist_domain_events()` application helper.
- Do not introduce a Unit of Work.
- Do not introduce an Event Bus.
- Do not introduce an Outbox.
- Do not introduce transaction coordination.
- Do not refactor unrelated use cases.
- Implement only the minimum behavior required for reopen-event persistence.

## Definition of Done

- RED → GREEN → REFACTOR
- Tests added
- Existing tests remain green
- Ruff passes
- MyPy passes
