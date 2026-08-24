# CORE-106 — Persist Investigation Claims

## Status

Done

## Context

Claims are now owned through the investigation aggregate, but the SQLite
investigation repository stores only investigations, hypotheses, and evidence.
Saving and reconstructing an aggregate therefore loses all claims.

## Goal

Persist and restore evidence-grounded claims as part of SQLite investigation
aggregate state.

## Acceptance Criteria

- Repository initialization creates a `claims` table when absent.
- Saving an investigation stores claim ID, hypothesis owner, statement, and
  evidence reference.
- `get()` restores claims in insertion order with original identities and text.
- `list()` restores the same claim state.
- Restored claims retain their evidence reference.
- Restoration leaves no pending `ClaimAdded` events.
- Existing databases without a claims table initialize safely.
- Existing investigation, hypothesis, and evidence persistence remains intact.
- No application use case or domain-event-store support is introduced.
- The complete test suite and quality gates pass.

## Out of Scope

- Claim domain-event persistence.
- Application orchestration.
- Claim removal, editing, status, or interpretation.
- Schema repair beyond creating the new table.

## Architectural Notes

Claims are stored beneath their owning hypothesis. Evidence is restored before
claims so the existing provenance invariant is applied during reconstruction.

## Validation

- Targeted SQLite investigation repository tests — 27 passed
- pytest — 225 passed
- Ruff lint — passed
- Ruff format — 190 files already formatted
- mypy — 69 source files checked
