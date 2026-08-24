# CORE-103 — Introduce Evidence-Grounded Claim

## Status

Done

## Context

TITAN currently preserves source-grounded evidence and its relationship to a
hypothesis, but it cannot represent an atomic statement extracted from that
evidence separately from the evidence description itself.

The accepted ubiquitous language names that atomic statement a `Claim`.

## Goal

Introduce the minimum domain model for an evidence-grounded claim.

## Acceptance Criteria

- A claim has its own generated `ClaimId`.
- A claim records a non-blank statement.
- A claim explicitly identifies its supporting `EvidenceId`.
- Original validated statement text is preserved.
- An explicit `ClaimId` can be supplied during reconstruction.
- Two separately created claims receive distinct identities.
- No aggregate integration, persistence, event, or application API changes.
- The complete test suite and quality gates pass.

## Out of Scope

- Attaching claims to hypotheses or investigations.
- Claim status, confidence, contradiction, or interpretation.
- SQLite persistence and domain events.
- Automatic extraction or AI integration.
- Claims supported by multiple evidence items.

## Architectural Notes

The first claim model is immutable and domain-neutral. Its evidence reference
preserves provenance without duplicating source metadata from `Evidence`.

## Validation

- Targeted claim domain tests — 4 passed
- pytest — 213 passed
- Ruff lint — passed
- Ruff format — 185 files already formatted
- mypy — 67 source files checked
