# CORE-142 — Reject Restored Duplicate Assessment Identities

## Context

Live aggregate mutation rejects duplicate assessment identities, and
`Investigation.restore()` contains the corresponding invariant, but focused
regression coverage does not yet prove that persisted reconstruction cannot
silently accept two assessments with the same identity.

## Goal

Lock down assessment identity uniqueness during aggregate restoration.

## Acceptance Criteria

- Restoration rejects two assessments with the same `AssessmentId`.
- The assessments may contain different narratives while sharing the identity.
- Restoration accepts distinct assessment identities for an owned thesis.
- Successful restoration emits no domain events.
- No production behavior, schema, API, or dependency changes.
- The complete quality gates pass.

## Out of Scope

- Assessment narrative uniqueness.
- Missing-thesis persistence diagnostics.
- Verdicts, scores, confidence values, or automatic decisions.
- HTTP, CLI, or AI integration.

## Architectural Notes

Identity, not narrative equality, defines duplicate assessment records. The
investigation remains the restoration boundary for aggregate-wide uniqueness.

## Validation

- Restored assessment identity tests — 2 passed
- pytest — 320 passed
- Ruff lint — passed
- Ruff format — passed
- mypy — passed
- GitHub Actions CI — passed
