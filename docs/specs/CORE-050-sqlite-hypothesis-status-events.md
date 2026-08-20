# CORE-050 — Add SQLite Support for Hypothesis Status Events

## User Story

As the application,
I want hypothesis status domain events to be stored by the SQLite domain event repository,
so that hypothesis confirmation and rejection events can be durably persisted.

## Acceptance Criteria

- `SqliteDomainEventRepository` supports `HypothesisConfirmed`.
- `SqliteDomainEventRepository` supports `HypothesisRejected`.
- A persisted `HypothesisConfirmed` event can be restored through `list_all()`.
- A persisted `HypothesisRejected` event can be restored through `list_all()`.
- The original `HypothesisId` is preserved for both event types.
- Hypothesis status events do not require an `InvestigationId`.
- Existing investigation domain event persistence remains unchanged.
- Existing hypothesis-added and hypothesis-removed event persistence remains unchanged.
- Event ordering remains unchanged.

## Technical Notes

- `HypothesisConfirmed` and `HypothesisRejected` contain only `hypothesis_id`.
- The SQLite representation must allow domain events that do not have an `investigation_id`.
- Do not invent an `InvestigationId` for hypothesis status events.
- Do not modify the domain events to satisfy infrastructure requirements.
- Do not introduce a Unit of Work.
- Do not introduce an Event Bus.
- Do not introduce an Outbox.
- Do not introduce application use-case changes in this story.
- Existing database migration support is outside the scope of this story.
- Implement only the minimum SQLite changes required to persist and restore the two status events.

## Definition of Done

- RED → GREEN → REFACTOR
- Tests added for `HypothesisConfirmed`
- Tests added for `HypothesisRejected`
- Existing tests remain green
- Ruff passes
- MyPy passes
