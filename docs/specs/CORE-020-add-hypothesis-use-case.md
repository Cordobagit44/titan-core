# CORE-020: Add Hypothesis Use Case

## User Story

As a client of the application,
I want to add a hypothesis to an investigation,
so that the application coordinates the operation.

## Acceptance Criteria

- An `AddHypothesis` use case exists.
- It receives an `InvestigationRepository`.
- It loads an investigation by identifier.
- It adds a hypothesis to the investigation.
- It saves the investigation.
- It returns the created hypothesis.
- A `LookupError` is raised if the investigation does not exist.
- Existing behavior remains unchanged.
