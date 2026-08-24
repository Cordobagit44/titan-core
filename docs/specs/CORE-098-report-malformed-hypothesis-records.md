# CORE-098 — Report Malformed Hypothesis Records

## Status

Done

## Context

CORE-097 adds contextual diagnostics for primary investigation records. Nested
SQLite hypothesis records with malformed identifiers or statuses still expose
low-level parser errors without identifying the persisted record field.

## Goal

Report malformed hypothesis identifier and status values with explicit record
and field context while retaining the original parser exception as the cause.

## Acceptance Criteria

- Valid persisted hypotheses continue to reconstruct normally.
- A malformed hypothesis identifier raises a contextual `ValueError`.
- A malformed hypothesis status raises a contextual `ValueError`.
- The error identifies the malformed persisted field and, when available, the
  hypothesis identifier.
- Existing persistence, ordering, migration, and restoration behavior remains
  unchanged.
- No public signature, schema, or dependency changes.
- The complete test suite and quality gates pass.

## Out of Scope

- Repairing malformed values.
- Diagnostics for evidence records.
- Validating hypothesis statements restored from legacy storage.
- Changing database constraints or schemas.

## Architectural Notes

Private repository parsing helpers translate low-level parser failures at the
SQLite deserialization boundary and preserve exception chaining.

## Validation

- Targeted SQLite investigation repository tests — 17 passed
- pytest — 197 passed
- Ruff lint — passed
- Ruff format — 178 files already formatted
- mypy — 65 source files checked
