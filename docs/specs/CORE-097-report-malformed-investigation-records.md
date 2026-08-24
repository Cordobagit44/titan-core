# CORE-097 — Report Malformed Investigation Records

## Status

Done

## Context

SQLite investigation records with malformed identifiers, statuses, or closure
timestamps currently expose low-level parser errors without identifying the
persisted record field that failed.

## Goal

Report malformed investigation record values with explicit record and field
context while retaining the original parser exception as the cause.

## Acceptance Criteria

- Valid persisted investigations continue to reconstruct normally.
- A malformed investigation identifier raises a contextual `ValueError`.
- A malformed investigation status raises a contextual `ValueError`.
- A malformed closure timestamp raises a contextual `ValueError`.
- The error identifies the malformed persisted field and, when available, the
  investigation identifier.
- Existing persistence, ordering, migration, and restoration behavior remains
  unchanged.
- No public signature, schema, or dependency changes.
- The complete test suite and quality gates pass.

## Out of Scope

- Repairing malformed values.
- Diagnostics for nested hypothesis or evidence records.
- Changing database constraints or schemas.
- Enforcing new domain lifecycle invariants during restoration.

## Architectural Notes

Private repository parsing helpers translate low-level parser failures at the
SQLite deserialization boundary and preserve exception chaining.

## Validation

- Targeted SQLite investigation repository tests — 15 passed
- pytest — 195 passed
- Ruff lint — passed
- Ruff format — 177 files already formatted
- mypy — 65 source files checked
