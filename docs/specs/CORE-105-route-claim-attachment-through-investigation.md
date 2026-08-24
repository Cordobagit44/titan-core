# CORE-105 — Route Claim Attachment Through Investigation

## Status

Done

## Context

CORE-104 lets a hypothesis own evidence-grounded claims. Direct hypothesis
mutation bypasses the owning investigation lifecycle, just as earlier direct
evidence and decision mutations once bypassed closed-investigation protection.

## Goal

Route claim attachment through the `Investigation` aggregate.

## Acceptance Criteria

- An open investigation delegates claim attachment to the selected hypothesis.
- Successful attachment returns the owning hypothesis.
- A closed investigation rejects claim attachment before mutation.
- An unknown hypothesis identifier raises `LookupError`.
- Existing claim provenance, duplicate identity, and hypothesis-status
  invariants remain delegated to `Hypothesis`.
- Successful attachment continues to emit `ClaimAdded` from the hypothesis.
- Rejected attachment produces no claim or event.
- No application use case, persistence, schema, or dependency changes.
- The complete test suite and quality gates pass.

## Out of Scope

- Application orchestration and Unit of Work integration.
- Claim persistence and event-store serialization.
- Claim removal or updates.
- Automatic extraction or AI integration.

## Architectural Notes

`Investigation` protects aggregate lifecycle and target lookup; `Hypothesis`
retains responsibility for claim provenance, identity, and decision state.

## Validation

- Targeted investigation claim tests — 3 passed
- pytest — 223 passed
- Ruff lint — passed
- Ruff format — 189 files already formatted
- mypy — 69 source files checked
