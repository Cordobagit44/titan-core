# CORE-048 — Persist Hypothesis Added Domain Event

## User Story

As the application,
I want domain events produced when a hypothesis is added to be persisted,
so that the creation of a new hypothesis is durably recorded after the use case completes.

## Acceptance Criteria

- `AddHypothesis` receives an `InvestigationRepository`.
- `AddHypothesis` also receives a `DomainEventRepository`.
- Adding a hypothesis still loads the investigation by identifier.
- A missing investigation still raises `LookupError`.
- Adding the hypothesis still creates and attaches the new hypothesis to the investigation.
- The investigation is still saved after adding the hypothesis.
- The `HypothesisAdded` event produced by the aggregate is persisted.
- The persisted event preserves the hypothesis statement.
- The created hypothesis is still returned.
- Existing domain behavior remains unchanged.
- Existing persistence abstractions remain unchanged.

## Technical Notes

- Reuse the existing `persist_domain_events()` application helper.
- Do not introduce a Unit of Work.
- Do not introduce an Event Bus.
- Do not introduce an Outbox.
- Do not introduce transaction coordination.
- Do not refactor unrelated use cases.
- Implement only the minimum behavior required for hypothesis-added event persistence.

## Definition of Done

- RED → GREEN → REFACTOR
- Tests added
- Existing tests remain green
- Ruff passes
- MyPy passes
