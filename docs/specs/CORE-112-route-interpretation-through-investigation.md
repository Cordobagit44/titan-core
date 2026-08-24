# CORE-112 — Route Interpretation Through Investigation

## Status

Done

## Context

CORE-111 lets a hypothesis own interpretations, but direct mutation bypasses
the owning investigation lifecycle and hypothesis lookup boundary.

## Goal

Route interpretation attachment through the `Investigation` aggregate.

## Acceptance Criteria

- An open investigation delegates attachment to the selected hypothesis.
- Successful attachment returns the owning hypothesis.
- A closed investigation rejects attachment before mutation.
- An unknown hypothesis identifier raises `LookupError`.
- Interpretation reference, identity, and hypothesis-status invariants remain
  delegated to `Hypothesis`.
- Successful attachment continues to emit `InterpretationAdded`.
- Rejected attachment produces no interpretation or event.
- No application use case, persistence, schema, or dependency changes.
- The complete test suite and quality gates pass.

## Out of Scope

- Application orchestration and Unit of Work integration.
- SQLite and event-store persistence.
- Interpretation removal, updates, scoring, or automatic reasoning.

## Architectural Notes

`Investigation` protects aggregate lifecycle and target lookup; `Hypothesis`
retains interpretation reference, identity, and decision-state invariants.

## Validation

- Targeted investigation interpretation tests — 3 passed
- pytest — 247 passed
- Ruff lint — passed
- Ruff format — 202 files already formatted
- mypy — 75 source files checked
