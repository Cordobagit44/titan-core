# CORE-051 — Persist Confirmed Hypothesis Domain Event

## User Story

As the application,
I want domain events produced when a hypothesis is confirmed to be persisted,
so that hypothesis confirmation is durably recorded after the use case completes.

## Acceptance Criteria

- `ConfirmHypothesis` receives an `InvestigationRepository`.
- `ConfirmHypothesis` also receives a `DomainEventRepository`.
- Confirming a hypothesis still loads the investigation by identifier.
- A missing investigation still raises `LookupError`.
- A missing hypothesis still raises `LookupError`.
- Confirming the hypothesis still changes its status to `CONFIRMED`.
- The investigation is still saved after confirming the hypothesis.
- The `HypothesisConfirmed` event produced by the hypothesis entity is persisted.
- The persisted event preserves the original `HypothesisId`.
- The confirmed hypothesis is still returned.
- Existing domain behavior remains unchanged.
- Existing persistence abstractions remain unchanged.

## Technical Notes

- Reuse the existing `persist_domain_events()` application helper.
- Persist pending events from the `Hypothesis` entity, not from the `Investigation`.
- Do not introduce a Unit of Work.
- Do not introduce an Event Bus.
- Do not introduce an Outbox.
- Do not introduce transaction coordination.
- Do not refactor unrelated use cases.
- Implement only the minimum behavior required for hypothesis-confirmed event persistence.

## Definition of Done

- RED → GREEN → REFACTOR
- Tests added
- Existing tests remain green
- Ruff passes
- MyPy passes
