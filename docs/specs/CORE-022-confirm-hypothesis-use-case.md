# CORE-022: Confirm Hypothesis Use Case

## User Story

As a client of the application,
I want to confirm a hypothesis,
so that the application coordinates the operation.

## Acceptance Criteria

- A `ConfirmHypothesis` use case exists.
- It receives an `InvestigationRepository`.
- It loads an investigation.
- It finds the requested hypothesis.
- It confirms the hypothesis.
- It saves the investigation.
- It returns the confirmed hypothesis.
- A `LookupError` is raised if the investigation does not exist.
- A `LookupError` is raised if the hypothesis does not exist.
- Existing behavior remains unchanged.
