# CORE-104 — Attach Claims to Hypotheses

## Status

Done

## Context

CORE-103 introduces an evidence-grounded `Claim`, but claims are not yet owned
by a reasoning structure. A hypothesis already owns the evidence from which a
claim is derived and is therefore the narrowest stable ownership boundary.

## Goal

Allow pending hypotheses to own claims grounded in evidence they already own.

## Acceptance Criteria

- A hypothesis exposes claims as an immutable tuple.
- A pending hypothesis accepts a claim whose `EvidenceId` it owns.
- Adding a claim emits `ClaimAdded` with hypothesis, claim, and evidence IDs.
- A claim referencing unknown evidence is rejected without mutation or event.
- Reusing a `ClaimId` in one hypothesis is rejected without mutation or event.
- Confirmed and rejected hypotheses cannot accept claims.
- Claim statement equality does not imply identity equality.
- No investigation integration, application use case, or persistence changes.
- The complete test suite and quality gates pass.

## Out of Scope

- SQLite and domain-event persistence for claims.
- Application use cases.
- Claim removal, status, confidence, contradiction, or interpretation.
- Claims grounded in multiple evidence items.
- Automatic claim extraction or AI integration.

## Architectural Notes

`Hypothesis` owns both evidence and derived claims. Evidence membership is
verified before mutation so claim provenance cannot point outside its owner.

## Validation

- Targeted hypothesis claim tests — 7 passed
- pytest — 220 passed
- Ruff lint — passed
- Ruff format — 187 files already formatted
- mypy — 68 source files checked
