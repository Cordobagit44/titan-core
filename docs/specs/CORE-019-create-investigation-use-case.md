# CORE-019: Create Investigation Use Case

## User Story

As a client of the application,
I want to create an investigation through a use case,
so that investigation creation is coordinated by the application layer.

## Acceptance Criteria

- A `CreateInvestigation` use case exists.
- It receives an `InvestigationRepository`.
- It creates an investigation from a title and purpose.
- It saves the created investigation in the repository.
- It returns the created investigation.
- Existing behavior remains unchanged.
