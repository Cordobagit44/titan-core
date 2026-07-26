# CORE-024: Add Evidence Use Case

## User Story

As a client of the application,
I want to add evidence to a hypothesis,
so that the application coordinates the operation.

## Acceptance Criteria

- An `AddEvidence` use case exists.
- It receives an `InvestigationRepository`.
- It loads an investigation.
- It finds the requested hypothesis.
- It adds evidence to the hypothesis.
- It saves the investigation.
- It returns the created evidence.
- A `LookupError` is raised if the investigation does not exist.
- A `LookupError` is raised if the hypothesis does not exist.
- Existing behavior remains unchanged.
