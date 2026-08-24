# CORE-099 — Report Malformed Evidence Records

## Status

Done

## Context

CORE-097 and CORE-098 add contextual diagnostics for investigation and
hypothesis records. Nested SQLite evidence records with malformed identifiers
or relationships still expose low-level parser errors without identifying the
persisted field.

## Goal

Report malformed evidence identifier and relationship values with explicit
record and field context while retaining the original parser exception.

## Acceptance Criteria

- Valid persisted evidence continues to reconstruct normally.
- A malformed evidence identifier raises a contextual `ValueError`.
- A malformed evidence relationship raises a contextual `ValueError`.
- The error identifies the malformed field and, when available, evidence ID.
- Existing persistence, ordering, migration, and restoration remain unchanged.
- No public signature, schema, or dependency changes.
- The complete test suite and quality gates pass.

## Out of Scope

- Repairing malformed values.
- Validating restored evidence descriptions or sources.
- Changing database constraints or schemas.

## Architectural Notes

Private parsing helpers translate failures at the SQLite deserialization
boundary and preserve exception chaining.

## Validation

- Targeted SQLite investigation repository tests — 19 passed
- pytest — 199 passed
- Ruff lint — passed
- Ruff format — 179 files already formatted
- mypy — 65 source files checked
