# CORE-115 — Add Interpretation Use Case

## Goal

Expose transactional interpretation creation through the application layer.

## Acceptance Criteria

- The application accepts an investigation, hypothesis, claim, and rationale.
- A successful operation attaches and returns a new `Interpretation`.
- Aggregate state and `InterpretationAdded` persist through one Unit of Work.
- Missing investigations and invalid hypothesis or claim references roll back.
- Domain-event persistence failures roll back without committing.
- `TitanApplication` exposes the use case through `bootstrap()`.

## Architectural Notes

The application creates the interpretation and coordinates persistence. The
investigation and hypothesis continue to enforce lifecycle, ownership, and
reference invariants. No HTTP, CLI, automatic interpretation, scoring, or AI
provider behavior is introduced.
