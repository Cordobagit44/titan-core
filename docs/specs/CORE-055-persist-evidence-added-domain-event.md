# CORE-055 — Persist Evidence Added Domain Event

## User Story

As the application,
I want domain events produced when evidence is added to a hypothesis to be persisted,
so that evidence additions are durably recorded after the use case completes.

## Acceptance Criteria

- `AddEvidence` receives an `InvestigationRepository`.
- `AddEvidence` also receives a `DomainEventRepository`.
- Adding evidence still loads the investigation by identifier.
- A missing investigation still raises `LookupError`.
- A missing hypothesis still raises `LookupError`.
- Evidence description validation remains unchanged.
- Evidence is still added to the selected hypothesis.
- The investigation is still saved after adding the evidence.
- The `EvidenceAdded` event produced by the hypothesis entity is persisted.
- The persisted event preserves the original `HypothesisId`.
- The persisted event preserves the original `EvidenceId`.
- The created evidence is still returned.
- Existing domain behavior remains unchanged.
- Existing persistence abstractions remain unchanged.

## Technical Notes

- Reuse the existing `persist_domain_events()` application helper.
- Persist pending events from the `Hypothesis` entity, not from the `Investigation`.
- Reuse SQLite support for `EvidenceAdded` introduced in CORE-054.
- Do not introduce a Unit of Work.
- Do not introduce an Event Bus.
- Do not introduce an Outbox.
- Do not introduce transaction coordination.
- Do not refactor unrelated use cases.
- Implement only the minimum behavior required for `EvidenceAdded` persistence.

## Definition of Done

- RED → GREEN → REFACTOR
- Tests added
- Existing tests remain green
- Ruff passes
- MyPy passes
