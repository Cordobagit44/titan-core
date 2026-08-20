# CORE-049 — Persist Hypothesis Removed Domain Event

## User Story

As the application,
I want domain events produced when a hypothesis is removed to be persisted,
so that hypothesis removal is durably recorded after the use case completes.

## Acceptance Criteria

- `RemoveHypothesis` receives an `InvestigationRepository`.
- `RemoveHypothesis` also receives a `DomainEventRepository`.
- Removing a hypothesis still loads the investigation by identifier.
- A missing investigation still raises `LookupError`.
- A missing hypothesis still raises `LookupError`.
- Removing the hypothesis still removes it from the investigation.
- The investigation is still saved after removing the hypothesis.
- The `HypothesisRemoved` event produced by the aggregate is persisted.
- The persisted event preserves the removed `HypothesisId`.
- Existing domain behavior remains unchanged.
- Existing persistence abstractions remain unchanged.

## Technical Notes

- Reuse the existing `persist_domain_events()` application helper.
- Do not introduce a Unit of Work.
- Do not introduce an Event Bus.
- Do not introduce an Outbox.
- Do not introduce transaction coordination.
- Do not refactor unrelated use cases.
- Implement only the minimum behavior required for hypothesis-removed event persistence.

## Definition of Done

- RED → GREEN → REFACTOR
- Tests added
- Existing tests remain green
- Ruff passes
- MyPy passes
