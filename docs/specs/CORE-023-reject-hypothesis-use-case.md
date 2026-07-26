# CORE-023: Reject Hypothesis Use Case

## User Story

As a client of the application,
I want to reject a hypothesis,
so that the application coordinates the operation.

## Acceptance Criteria

- A `RejectHypothesis` use case exists.
- It receives an `InvestigationRepository`.
- It loads an investigation.
- It finds the requested hypothesis.
- It rejects the hypothesis.
- It saves the investigation.
- It returns the rejected hypothesis.
- A `LookupError` is raised if the investigation does not exist.
- A `LookupError` is raised if the hypothesis does not exist.
- Existing behavior remains unchanged.
