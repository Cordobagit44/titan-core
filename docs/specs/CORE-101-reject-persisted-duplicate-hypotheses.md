# CORE-101 — Reject Persisted Duplicate Hypotheses

## Status

Done

## Context

Investigation creation rejects hypothesis statements that are equal after
trimming leading and trailing whitespace. Aggregate restoration currently
bypasses that invariant and can reconstruct invalid persisted state.

## Goal

Apply the established hypothesis statement uniqueness invariant when restoring
an investigation.

## Acceptance Criteria

- Restoration rejects exact duplicate hypothesis statements.
- Restoration rejects statements equivalent after trimming edge whitespace.
- Comparison remains case-sensitive.
- Valid restored hypotheses retain their original statement text and status.
- Rejected restoration emits no domain events.
- SQLite retrieval propagates rejection of persisted duplicate hypotheses.
- No public signature, schema, event type, or dependency changes.
- The complete test suite and quality gates pass.

## Out of Scope

- Repairing or merging historical duplicates.
- Case-insensitive comparison.
- Collapsing internal whitespace.
- Database uniqueness constraints.

## Architectural Notes

Hypothesis statement uniqueness remains an aggregate invariant shared by new
mutation and restoration paths.

## Validation

- Targeted domain and SQLite repository tests — 59 passed
- pytest — 208 passed
- Ruff lint — passed
- Ruff format — 181 files already formatted
- mypy — 65 source files checked
