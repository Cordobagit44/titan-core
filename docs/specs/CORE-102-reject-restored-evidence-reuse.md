# CORE-102 — Reject Restored Evidence Reuse

## Status

Done

## Context

An investigation prevents one evidence identity from being added to multiple
hypotheses. Aggregate restoration currently bypasses that ownership invariant
when supplied preconstructed hypotheses.

## Goal

Reject restored investigations where the same evidence identifier belongs to
more than one hypothesis.

## Acceptance Criteria

- Restoration rejects evidence identifiers reused across hypotheses.
- Rejection uses the established aggregate ownership error.
- Distinct evidence identifiers remain restorable.
- Rejected restoration emits no investigation domain events.
- Existing SQLite behavior remains unchanged; its evidence primary key already
  prevents duplicate identifiers.
- No public signature, schema, event type, or dependency changes.
- The complete test suite and quality gates pass.

## Out of Scope

- Cross-investigation evidence identity rules.
- Repairing or cloning shared historical evidence.
- Database schema changes.
- Evidence semantic duplicate detection.

## Architectural Notes

Evidence identity ownership remains an `Investigation` aggregate invariant
shared by mutation and restoration paths.

## Validation

- Targeted investigation domain tests — 35 passed
- pytest — 209 passed
- Ruff lint — passed
- Ruff format — 182 files already formatted
- mypy — 65 source files checked
