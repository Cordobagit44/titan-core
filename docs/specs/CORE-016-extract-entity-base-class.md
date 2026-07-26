# CORE-016: Extract entity base class

## User Story

As a developer,
I want entities to share common event management behavior,
so that duplicated code is removed from the domain model.

## Acceptance Criteria

- A base `Entity` class exists.
- `Entity` manages domain events.
- `Investigation` inherits from `Entity`.
- `Hypothesis` inherits from `Entity`.
- Existing behavior remains unchanged.
- All existing tests continue to pass.
