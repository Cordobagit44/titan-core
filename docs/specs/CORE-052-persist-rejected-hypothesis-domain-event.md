# CORE-052 — Persist Rejected Hypothesis Domain Event

## User Story

As the application,
I want domain events produced when a hypothesis is rejected to be persisted,
so that hypothesis rejection is durably recorded after the use case completes.

## Acceptance Criteria

- `RejectHypothesis` receives an `InvestigationRepository`.
- `RejectHypothesis` also receives a `DomainEventRepository`.
- Rejecting a hypothesis still loads the investigation by identifier.
- A missing investigation still raises `LookupError`.
- A missing hypothesis still raises `LookupError`.
- Rejecting the hypothesis still changes its status to `REJECTED`.
- The investigation is still saved after rejecting the hypothesis.
- The `HypothesisRejected` event produced by the hypothesis entity is persisted.
- The persisted event preserves the original `HypothesisId`.
- The rejected hypothesis is still returned.
- Existing domain behavior remains unchanged.
- Existing persistence abstractions remain unchanged.

## Technical Notes

- Reuse the existing `persist_domain_events()` application helper.
- Persist pending events from the `Hypothesis` entity, not from the `Investigation`.
- Reuse SQLite support for `HypothesisRejected` introduced in CORE-050.
- Do not introduce a Unit of Work.
- Do not introduce an Event Bus.
- Do not introduce an Outbox.
- Do not introduce transaction coordination.
- Do not refactor unrelated use cases.
- Implement only the minimum behavior required for hypothesis-rejected event persistence.

## Definition of Done

- RED → GREEN → REFACTOR
- Tests added
- Existing tests remain green
- Ruff passes
- MyPy passes
