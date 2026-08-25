# CORE-133 — Reject Restored Duplicate Thesis Identities

## Context

Live investigation mutation rejects reuse of a thesis identity, and repository
reconstruction already validates the same invariant. That restoration boundary
lacks focused regression coverage.

## Goal

Prove that an investigation cannot be restored with duplicate thesis identities.

## Acceptance Criteria

- Restoration rejects two theses carrying the same `ThesisId`.
- Different statements do not permit reuse of one identity.
- Rejection occurs before a reconstructed aggregate or pending event can escape.
- Distinct thesis identities remain valid.
- No persistence schema, application API, or dependency changes.
- The complete quality gates pass.

## Out of Scope

- Cross-investigation global identity coordination.
- Thesis selection, removal, status, versioning, or assessment.
- Data repair.

## Architectural Notes

Identity uniqueness is enforced inside one reconstructed investigation
aggregate, matching the live mutation rule.

## Validation

- Restored thesis identity tests — 2 passed
- pytest — 292 passed
- Ruff lint — passed
- Ruff format — passed
- mypy — passed
- GitHub Actions CI — passed
