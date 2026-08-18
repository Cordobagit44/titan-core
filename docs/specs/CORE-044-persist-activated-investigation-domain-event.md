# CORE-044 — Persist Activated Investigation Domain Event

## User Story

As the application,
I want domain events produced during investigation activation to be persisted,
so that meaningful domain facts are not lost after the use case completes.

## Acceptance Criteria

- `ActivateInvestigation` receives an `InvestigationRepository`.
- `ActivateInvestigation` also receives a `DomainEventRepository`.
- Activating an investigation still loads the investigation by identifier.
- A missing investigation still raises `LookupError`.
- Activating the investigation still changes its domain state.
- The investigation is still saved after activation.
- The `InvestigationActivated` event produced by the aggregate is persisted.
- The activated investigation is still returned.
- Existing domain behavior remains unchanged.
- Existing persistence abstractions remain unchanged.

## Technical Notes

- Do not introduce a Unit of Work.
- Do not introduce an Event Bus.
- Do not introduce an Outbox.
- Do not introduce generalized event dispatch yet.
- Do not refactor `CreateInvestigation` as part of this story.
- Implement only the minimum behavior required for activation event persistence.

## Definition of Done

- RED → GREEN → REFACTOR
- Tests added
- Existing tests remain green
- Ruff passes
- MyPy passes
