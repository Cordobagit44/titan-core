# CORE-122 — Report Malformed Interpretation Records

## Goal

Report malformed persisted interpretation identifier fields with explicit
record and field context.

## Acceptance Criteria

- Valid persisted interpretations continue to reconstruct normally.
- A malformed interpretation identifier raises a contextual `ValueError`.
- A malformed interpretation claim identifier raises a contextual `ValueError`.
- The error identifies the malformed field and, when available, the
  interpretation ID.
- Existing persistence, ordering, restoration, and ownership behavior remains
  unchanged.

## Out of Scope

- Repairing malformed values.
- Validating persisted interpretation rationale text.
- Changing database constraints or schemas.
- Claim record diagnostics already completed by CORE-121.

## Architectural Notes

Private parsing helpers translate UUID failures at the SQLite deserialization
boundary and preserve exception chaining. No public API, schema, event,
scoring, or AI behavior is introduced.
