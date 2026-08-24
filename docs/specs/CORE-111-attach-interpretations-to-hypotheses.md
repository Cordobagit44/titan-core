# CORE-111 — Attach Interpretations to Hypotheses

## Status

Done

## Context

CORE-110 introduces an explicit interpretation, but it has no owning reasoning
boundary. Each interpretation already identifies one hypothesis and one claim,
and the hypothesis owns that claim.

## Goal

Allow pending hypotheses to own interpretations that reference themselves and
one of their existing claims.

## Acceptance Criteria

- A hypothesis exposes interpretations as an immutable tuple.
- A pending hypothesis accepts an interpretation targeting itself and an owned
  claim.
- Adding an interpretation emits `InterpretationAdded` with hypothesis,
  interpretation, and claim IDs.
- A mismatched hypothesis reference is rejected without mutation or event.
- An unknown claim reference is rejected without mutation or event.
- Reusing an `InterpretationId` in one hypothesis is rejected.
- Confirmed and rejected hypotheses cannot accept interpretations.
- Equal rationale does not collapse distinct interpretation identities.
- No investigation routing, persistence, or application API changes.
- The complete test suite and quality gates pass.

## Out of Scope

- SQLite and event-store persistence.
- Application use cases.
- Interpretation removal, status, confidence, or scoring.
- Multi-claim interpretations and automatic reasoning.

## Architectural Notes

`Hypothesis` owns claims and the interpretations that reason from them. All
references are validated before mutation to prevent dangling reasoning links.

## Validation

- Targeted hypothesis interpretation tests — 8 passed
- pytest — 244 passed
- Ruff lint — passed
- Ruff format — 200 files already formatted
- mypy — 74 source files checked
