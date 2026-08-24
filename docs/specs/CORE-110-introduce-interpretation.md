# CORE-110 — Introduce Interpretation

## Status

Done

## Context

TITAN can now preserve atomic claims grounded in evidence, but it cannot
represent the reasoning that connects a claim to a hypothesis. The accepted
ubiquitous language names that reasoned relationship an `Interpretation`.

## Goal

Introduce the minimum immutable domain model for an interpretation connecting
one claim to one hypothesis with an explicit rationale.

## Acceptance Criteria

- An interpretation has a generated `InterpretationId`.
- It identifies exactly one `ClaimId` and one `HypothesisId`.
- It records a non-blank rationale explaining the relationship.
- Original validated rationale text is preserved.
- An explicit identity can be supplied during reconstruction.
- Separately created interpretations receive distinct identities.
- No ownership, persistence, event, or application API changes.
- The complete test suite and quality gates pass.

## Out of Scope

- Interpretation type, direction, strength, confidence, or status.
- Connecting multiple claims in one interpretation.
- Aggregate ownership and lifecycle rules.
- SQLite persistence and domain events.
- Automatic reasoning or AI integration.

## Architectural Notes

The single-claim link is the smallest explicit reasoning unit. More complex
reasoning can compose multiple interpretations without prematurely embedding a
graph or scoring model.

## Validation

- Targeted interpretation domain tests — 4 passed
- pytest — 236 passed
- Ruff lint — passed
- Ruff format — 198 files already formatted
- mypy — 73 source files checked
