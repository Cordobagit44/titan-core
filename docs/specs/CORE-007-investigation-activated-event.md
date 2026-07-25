# CORE-007 — Emit InvestigationActivated Event

## User Story

As a consumer of the domain,
I want to know when an investigation is activated,
so that other parts of the system can react to that change.

## Acceptance Criteria

- Activating an investigation emits one `InvestigationActivated` event.
- The event contains the investigation identifier.
- The creation event can be pulled before activation.
- After activation, `pull_events()` returns the activation event.
- A failed repeated activation does not emit another event.

## Technical Notes

- `InvestigationActivated` is immutable.
- The event contains `investigation_id`.
- The aggregate event queue supports both creation and activation events.
