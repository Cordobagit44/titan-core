# CORE-027: List Investigations Use Case

## User Story

As a client of the application,
I want to list all investigations,
so that I can browse existing investigations.

## Acceptance Criteria

- A `ListInvestigations` use case exists.
- `InvestigationRepository` exposes `list()`.
- `InMemoryInvestigationRepository` implements `list()`.
- It returns `tuple[Investigation, ...]`.
- It returns an empty tuple when there are no investigations.
- It does not modify repository state.
- Existing behavior remains unchanged.
