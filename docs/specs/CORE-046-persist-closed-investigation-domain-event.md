# CORE-046 — Persist Closed Investigation Domain Event

## User Story

As the application,
I want domain events produced during investigation closing to be persisted,
so that the closure of an investigation is durably recorded after the use case completes.

## Acceptance Criteria

- `CloseInvestigation` receives an `InvestigationRepository`.
- `CloseInvestigation` also receives a `DomainEventRepository`.
- Closing an investigation still loads the investigation by identifier.
- A missing investigation still raises `LookupError`.
- Closing the investigation still changes its domain state to `CLOSED`.
- The investigation is still saved after closing.
- The `InvestigationClosed` event produced by the aggregate is persisted.
- The persisted event preserves the same `closed_at` timestamp recorded by the investigation.
- The closed investigation is still returned.
- Existing domain behavior remains unchanged.
- Existing persistence abstractions remain unchanged.

## Technical Notes

- Reuse the existing `persist_domain_events()` application helper.
- Do not introduce a Unit of Work.
- Do not introduce an Event Bus.
- Do not introduce an Outbox.
- Do not introduce transaction coordination.
- Do not refactor unrelated use cases.
- Implement only the minimum behavior required for close-event persistence.

## Definition of Done

- RED → GREEN → REFACTOR
- Tests added
- Existing tests remain green
- Ruff passes
- MyPy passes
