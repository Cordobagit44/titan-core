# CORE-017: Introduce Investigation Repository

## User Story

As the application,
I want a repository abstraction for investigations,
so that persistence is independent from the domain.

## Acceptance Criteria

- An `InvestigationRepository` abstraction exists.
- It can save an investigation.
- It can retrieve an investigation by identifier.
- No persistence implementation exists yet.
- Existing behavior remains unchanged.
