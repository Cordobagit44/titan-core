# CORE-026: Get Investigation Use Case

## User Story

As a client of the application,
I want to retrieve an investigation,
so that I can inspect its current state.

## Acceptance Criteria

- A `GetInvestigation` use case exists.
- It receives an `InvestigationRepository`.
- It returns the requested investigation.
- It raises `LookupError` if the investigation does not exist.
- It does not modify the investigation.
- It does not save the investigation.
- Existing behavior remains unchanged.
