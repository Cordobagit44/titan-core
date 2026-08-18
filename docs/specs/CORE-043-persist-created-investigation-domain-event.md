# CORE-043 — Persist Created Investigation Domain Event

## User Story

As the application,
I want domain events produced during investigation creation to be persisted,
so that meaningful domain facts are not lost after the use case completes.

## Acceptance Criteria

- `CreateInvestigation` receives an `InvestigationRepository`.
- `CreateInvestigation` also receives a `DomainEventRepository`.
- Creating an investigation still saves the investigation.
- The `InvestigationCreated` event produced by the aggregate is persisted.
- The created investigation is still returned.
- Existing domain behavior remains unchanged.
- Existing persistence abstractions remain unchanged.

## Technical Notes

- Do not introduce a Unit of Work.
- Do not introduce an Event Bus.
- Do not introduce an Outbox.
- Do not generalize event dispatch yet.
- Implement only the minimum behavior needed by this story.

## Definition of Done

- RED → GREEN → REFACTOR
- Tests added
- Existing tests remain green
- Ruff passes
- MyPy passes
