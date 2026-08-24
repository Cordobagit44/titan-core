# CORE-125 — Reject Broken Persisted Interpretation References

## Goal

Reject a persisted interpretation whose claim reference does not belong to its
hypothesis with explicit record context.

## Acceptance Criteria

- Valid persisted interpretations continue to reconstruct normally.
- A well-formed but unknown interpretation claim identifier is rejected.
- The error identifies the interpretation and missing claim relationship.
- The SQLite boundary raises a contextual `ValueError` while preserving the
  domain failure as its cause.
- Existing persistence, ordering, restoration, and ownership behavior remains
  unchanged.

## Out of Scope

- Repairing or deleting corrupted rows.
- Changing database constraints or schemas.
- Cross-hypothesis reference sharing.
- Claim evidence reference validation already completed by CORE-124.

## Architectural Notes

The repository translates the existing domain claim lookup failure while
reconstructing interpretations. No public API, schema, event, scoring, or AI
behavior is introduced.
