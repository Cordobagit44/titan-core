# CORE-010: Emit HypothesisAdded domain event

## User Story

As an investigator,
I want the investigation to emit an event whenever a hypothesis is added,
so that other parts of the system can react to that business action.

## Acceptance Criteria

- A new domain event named `HypothesisAdded` exists.
- The event contains:
  - `investigation_id`
  - `hypothesis_statement`
- Calling `Investigation.add_hypothesis()` emits exactly one `HypothesisAdded` event.
- The event is available through `pull_events()`.
- Existing behavior remains unchanged.
