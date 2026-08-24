# CORE-085 — Prevent Repeated Hypothesis Decisions

## Status

Done

## Context

A pending hypothesis may be confirmed or rejected, and opposite terminal
transitions are already rejected. However, confirming an already confirmed
hypothesis or rejecting an already rejected hypothesis currently succeeds and
emits another domain event even though authoritative state does not change.

Repeated decision events weaken the historical meaning of the event stream.

## Goal

Reject repeated hypothesis decisions before state or pending events change.

## Domain Behavior

- Confirming a confirmed hypothesis raises
  `ValueError("hypothesis is already confirmed")`.
- Rejecting a rejected hypothesis raises
  `ValueError("hypothesis is already rejected")`.
- A rejected hypothesis still cannot be confirmed.
- A confirmed hypothesis still cannot be rejected.
- Failed repeated decisions emit no domain event.

## Application Behavior

The existing `ConfirmHypothesis` and `RejectHypothesis` error paths propagate the
domain failure, roll back the Unit of Work, and do not commit.

## Acceptance Criteria

- Repeated confirmation is rejected without a new event.
- Repeated rejection is rejected without a new event.
- Application failures roll back and do not commit.
- Existing valid and opposite-terminal transitions remain unchanged.
- Ruff lint passes.
- Ruff format check passes.
- mypy passes.
- The complete pytest suite passes.

## Out of Scope

CORE-085 does not introduce:

- reversal of a confirmed or rejected decision;
- automatic decisions based on evidence;
- confidence or certainty scoring;
- assessment, claims, interpretations, or thesis modeling;
- persistence schema changes;
- new events or dependencies.

## Validation

- Targeted hypothesis decision tests — 30 passed
- `uv run ruff check .` — passed
- `uv run ruff format --check .` — 165 files already formatted
- `uv run mypy` — no issues in 65 source files
- `uv run pytest` — 166 passed
