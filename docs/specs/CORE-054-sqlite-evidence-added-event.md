# CORE-054 — Add SQLite Support for Evidence Added Event

## User Story

As the application,
I want `EvidenceAdded` domain events to be stored by the SQLite domain event repository,
so that evidence additions can be durably persisted and restored.

## Acceptance Criteria

- `SqliteDomainEventRepository` supports `EvidenceAdded`.
- A persisted `EvidenceAdded` event can be restored through `list_all()`.
- The original `HypothesisId` is preserved.
- The original `EvidenceId` is preserved.
- `EvidenceAdded` does not require an `InvestigationId`.
- Existing investigation domain event persistence remains unchanged.
- Existing hypothesis domain event persistence remains unchanged.
- Event ordering remains unchanged.

## Technical Notes

- `EvidenceAdded` contains `hypothesis_id` and `evidence_id`.
- Extend the SQLite event representation with an `evidence_id` column.
- Do not invent an `InvestigationId` for `EvidenceAdded`.
- Do not modify the domain event to satisfy infrastructure requirements.
- Do not modify `AddEvidence` in this story.
- Do not introduce a Unit of Work.
- Do not introduce an Event Bus.
- Do not introduce an Outbox.
- Do not introduce transaction coordination.
- Existing database migration support is outside the scope of this story.
- Implement only the minimum SQLite changes required to persist and restore `EvidenceAdded`.

## Definition of Done

- RED → GREEN → REFACTOR
- Test added for `EvidenceAdded`
- Existing tests remain green
- Ruff passes
- MyPy passes
