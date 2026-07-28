# CORE-040 — Emit InvestigationReopened Event

## Goal

As the domain,

I want reopening an investigation to emit an `InvestigationReopened` domain event,

so that external consumers can react to the state transition in a traceable way.

## Business Rules

- Reopening an investigation emits an `InvestigationReopened` event.
- The event is recorded exactly once per successful reopen operation.
- The investigation status becomes `ACTIVE`.
- The `closed_at` timestamp is cleared.
- Existing reopen behavior remains unchanged apart from emitting the event.

## Acceptance Criteria

- A new `InvestigationReopened` domain event exists.
- `Investigation.reopen()` records the event.
- Existing tests continue to pass.
- New tests verify the emitted event.
