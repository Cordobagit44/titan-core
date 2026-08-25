# CORE-141 — Cover Assessment Record Diagnostics

## Context

The SQLite repository parses assessment identity, thesis reference, and
narrative with contextual diagnostics, but these persistence-boundary
guarantees do not yet have focused regression coverage.

## Goal

Lock down explicit diagnostics for malformed persisted assessment records.

## Acceptance Criteria

- A malformed assessment identifier is rejected as an invalid persisted
  assessment id.
- A malformed thesis reference is rejected with the assessment identity and
  `thesis_id` field in the diagnostic.
- A blank persisted narrative is rejected with the assessment identity and
  narrative field in the diagnostic.
- Valid persisted assessment behavior remains unchanged.
- No production behavior, schema, API, or dependency changes.
- The complete quality gates pass.

## Out of Scope

- Missing-thesis referential integrity.
- Duplicate restored assessment identities.
- Verdicts, scores, confidence values, or automatic decisions.
- HTTP, CLI, or AI integration.

## Architectural Notes

These tests exercise the SQLite reconstruction boundary directly because the
requirement concerns corrupted persisted records rather than public creation.

## Validation

- Assessment record diagnostics tests — 3 passed
- pytest — 318 passed
- Ruff lint — passed
- Ruff format — passed
- mypy — passed
- GitHub Actions CI — passed
