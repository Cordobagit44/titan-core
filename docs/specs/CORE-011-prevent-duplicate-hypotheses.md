# CORE-011: Prevent duplicate hypotheses

## User Story

As an investigator,
I want an investigation to reject duplicate hypotheses,
so that each hypothesis remains unique within the investigation.

## Acceptance Criteria

- An investigation cannot contain two hypotheses with the same statement.
- Duplicate comparison uses the validated hypothesis statement.
- Attempting to add a duplicate hypothesis raises `ValueError`.
- The error message is `hypothesis already exists`.
- A rejected duplicate does not add a hypothesis.
- A rejected duplicate does not emit a `HypothesisAdded` event.
- Existing behavior remains unchanged.
