# CORE-121 — Report Malformed Claim Records

## Goal

Report malformed persisted claim identifier fields with explicit record and
field context.

## Acceptance Criteria

- Valid persisted claims continue to reconstruct normally.
- A malformed claim identifier raises a contextual `ValueError`.
- A malformed claim evidence identifier raises a contextual `ValueError`.
- The error identifies the malformed field and, when available, the claim ID.
- Existing persistence, ordering, restoration, and ownership behavior remains
  unchanged.

## Out of Scope

- Repairing malformed values.
- Validating persisted claim statement text.
- Changing database constraints or schemas.
- Interpretation record diagnostics.

## Architectural Notes

Private parsing helpers translate UUID failures at the SQLite deserialization
boundary and preserve exception chaining. No public API, schema, event,
scoring, or AI behavior is introduced.
