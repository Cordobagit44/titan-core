# CORE-012: Introduce HypothesisId

## User Story

As an investigator,
I want every hypothesis to have a stable identity,
so that hypotheses can be referenced and managed individually.

## Acceptance Criteria

- A new value object named `HypothesisId` exists.
- `HypothesisId` contains a UUID value.
- `HypothesisId.new()` creates a new identifier.
- Every `Hypothesis` has an `id`.
- Creating a `Hypothesis` assigns a new `HypothesisId` automatically.
- Two independently created hypotheses have different identifiers.
- Existing hypothesis validation remains unchanged.
- Existing investigation behavior remains unchanged.
