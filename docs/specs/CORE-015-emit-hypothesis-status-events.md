# CORE-015: Emit hypothesis status events

## User Story

As the system,
I want hypothesis status changes to emit domain events,
so that other parts of the application can react to them.

## Acceptance Criteria

- A `HypothesisConfirmed` domain event exists.
- A `HypothesisRejected` domain event exists.
- `Hypothesis.confirm()` emits `HypothesisConfirmed`.
- `Hypothesis.reject()` emits `HypothesisRejected`.
- Events are exposed through `Hypothesis.pull_events()`.
- Existing hypothesis behavior remains unchanged.
- Existing investigation behavior remains unchanged.
