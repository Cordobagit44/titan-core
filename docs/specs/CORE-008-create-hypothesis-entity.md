# CORE-008 — Create Hypothesis Entity

## User Story

As an investment analyst,
I want to create a hypothesis,
so that I can document an investment thesis that will later be validated or rejected.

## Acceptance Criteria

- A hypothesis has a statement.
- The statement must not be empty.
- A hypothesis is immutable after creation.
- Creating a hypothesis with an empty statement raises `ValueError`.

## Technical Notes

- Introduce a new domain entity named `Hypothesis`.
- The entity is independent for now.
- It will be associated with `Investigation` in CORE-009.
