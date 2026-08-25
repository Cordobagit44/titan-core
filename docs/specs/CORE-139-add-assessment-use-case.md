# CORE-139 — Add Assessment Use Case

## Goal

Expose transactional narrative assessment creation through the application layer.

## Acceptance Criteria

- The use case accepts investigation ID, thesis ID, and narrative.
- It returns a newly identified `Assessment`.
- Mutation routes through `Investigation.add_assessment()`.
- Aggregate state and `AssessmentAdded` persist through one Unit of Work.
- Missing investigation, unknown thesis, closed investigation, blank narrative,
  and event persistence failure roll back.
- `bootstrap()` exposes `add_assessment`.
- Existing transaction behavior remains intact.
- The complete quality gates pass.

## Out of Scope

- Verdicts, scores, percentages, selection, revision, or removal.
- Acceptance workflow expansion.
- HTTP, CLI, automation, or AI synthesis.

## Architectural Notes

The application creates the assessment and coordinates persistence. The
investigation remains authoritative for thesis ownership and lifecycle rules.
