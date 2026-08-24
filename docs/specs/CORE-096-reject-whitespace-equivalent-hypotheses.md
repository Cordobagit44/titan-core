# CORE-096 — Reject Whitespace-Equivalent Hypotheses

## Status

Done

## Context

Investigations reject hypotheses only when their stored statements are exactly
equal. Because hypothesis validation checks `statement.strip()` only for
emptiness, a statement surrounded by extra whitespace is accepted beside the
same visible statement without that whitespace.

## Goal

Treat hypothesis statements that differ only by leading or trailing whitespace
as duplicates within an investigation.

## Acceptance Criteria

- Exact duplicate statements remain rejected.
- Leading or trailing whitespace does not bypass duplicate detection.
- A rejected duplicate does not add a hypothesis or emit `HypothesisAdded`.
- The application use case rolls back and does not commit after rejection.
- Accepted hypothesis text remains stored exactly as supplied.
- Duplicate comparison remains case-sensitive.
- No public signature, schema, event type, or dependency changes.
- The complete test suite and quality gates pass.

## Out of Scope

- Lowercasing or case-insensitive comparison.
- Collapsing internal whitespace.
- Editing existing hypothesis statements.
- Migrating historical duplicates.

## Architectural Notes

The aggregate compares trimmed statements only for uniqueness. `Hypothesis`
continues to preserve the original validated statement.

## Validation

- Targeted investigation and add-hypothesis tests — 37 passed
- pytest — 192 passed
- Ruff lint — passed
- Ruff format — 176 files already formatted
- mypy — 65 source files checked
