# CORE-038 — Close Investigation Use Case

## Goal

Expose the investigation closing capability through the application layer.

The use case must delegate the business rules to the domain model and persist the updated investigation through the repository.

## Motivation

The domain already supports closing an investigation.

Application services should expose this behaviour without duplicating domain logic.

## Acceptance Criteria

- A `CloseInvestigation` use case exists.
- The use case retrieves the investigation from the repository.
- The investigation is closed through the domain model.
- The updated investigation is persisted.
- If the investigation does not exist, the use case raises an appropriate exception.
- Existing domain rules remain unchanged.
- All existing tests continue to pass.

## Technical Notes

- Follow the existing application use case pattern.
- Do not introduce domain logic into the application layer.
- Repository abstraction must remain unchanged.

## Definition of Done

- RED → GREEN → REFACTOR completed.
- pytest passes.
- Ruff passes.
- mypy passes.
- CHANGELOG updated.
- PROJECT_MEMORY updated if necessary.
