# CORE-091 — Prevent Duplicate Evidence

## Status

Done

## Context

A pending hypothesis currently accepts the same `Evidence` entity more than
once. Each addition appends the same evidence identifier and emits another
`EvidenceAdded` event. Persisting that aggregate can then conflict with the
SQLite primary key for evidence.

## Goal

Ensure each evidence identifier appears at most once within a hypothesis.

## Acceptance Criteria

- Adding new evidence to a pending hypothesis continues to succeed.
- Adding an evidence identifier already present raises
  `ValueError("evidence already exists")`.
- A rejected duplicate does not change the evidence collection.
- A rejected duplicate emits no `EvidenceAdded` event.
- Distinct evidence identifiers remain valid even when their descriptive fields
  match.
- Decided-hypothesis evidence protection remains unchanged.
- No public API, schema, event type, or dependency changes.
- The complete test suite and quality gates pass.

## Out of Scope

- Detecting semantic duplicates by description or source.
- Merging evidence records.
- Editing or deleting evidence.
- Cross-hypothesis evidence identity rules.

## Architectural Notes

The invariant belongs to `Hypothesis`, which owns its evidence collection. It
compares stable `EvidenceId` values rather than descriptive text.

## Validation

- Targeted hypothesis tests — 20 passed
- pytest — 179 passed
- Ruff lint — passed
- Ruff format — 171 files already formatted
- mypy — 65 source files checked
