# CORE-025: Refactor Investigation Loading

## User Story

As a maintainer,
I want investigation loading and validation to be centralized,
so that application use cases avoid duplicated logic.

## Acceptance Criteria

- A shared application helper loads an investigation from an
  `InvestigationRepository`.
- The helper returns the investigation when it exists.
- The helper raises `LookupError` when the investigation does not exist.
- Existing use cases delegate investigation loading to the helper.
- Public use case APIs remain unchanged.
- Existing error messages remain unchanged.
- Existing behavior remains unchanged.
- All tests continue to pass.
