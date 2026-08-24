# CORE-124 — Reject Broken Persisted Claim References

## Goal

Reject a persisted claim whose evidence reference does not belong to its
hypothesis with explicit record context.

## Acceptance Criteria

- Valid persisted claims continue to reconstruct normally.
- A well-formed but unknown claim evidence identifier is rejected.
- The error identifies the claim and the invalid evidence reference.
- The SQLite boundary raises a contextual `ValueError` while preserving the
  domain failure as its cause.
- Existing persistence, ordering, restoration, and ownership behavior remains
  unchanged.

## Out of Scope

- Repairing or deleting corrupted rows.
- Changing database constraints or schemas.
- Interpretation reference validation.
- Cross-hypothesis reference sharing.

## Architectural Notes

The repository translates the existing domain grounding failure while
reconstructing claims. No public API, schema, event, scoring, or AI behavior is
introduced.
