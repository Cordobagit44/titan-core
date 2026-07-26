# CORE-028: Remove Hypothesis Use Case

## User Story

As an investigator,
I want to remove a hypothesis,
so that incorrect or accidental hypotheses no longer belong to the investigation.

## Acceptance Criteria

- A `RemoveHypothesis` use case exists.
- It receives an `InvestigationRepository`.
- It removes an existing hypothesis from an investigation.
- It raises `LookupError` if the investigation does not exist.
- It raises `LookupError` if the hypothesis does not exist.
- It saves the investigation after removing the hypothesis.
- Removing a hypothesis records a `HypothesisRemoved` domain event.
- Existing behavior remains unchanged.
