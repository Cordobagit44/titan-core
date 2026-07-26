# CORE-021: Add Investigation.find_hypothesis()

## User Story

As the application,
I want an investigation to locate one of its hypotheses by identifier,
so that use cases do not depend on the aggregate's internal collection structure.

## Acceptance Criteria

- `Investigation` exposes `find_hypothesis`.
- It receives a `HypothesisId`.
- It returns the matching `Hypothesis`.
- It returns `None` when no matching hypothesis exists.
- Existing behavior remains unchanged.
