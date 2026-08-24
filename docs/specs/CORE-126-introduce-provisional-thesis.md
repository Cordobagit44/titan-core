# CORE-126 — Introduce Provisional Thesis

## Context

TITAN can preserve evidence-grounded claims and explicit interpretations, but
it cannot represent the provisional conclusion those reasoning structures may
eventually support. The accepted ubiquitous language names that conclusion a
`Thesis`.

## Goal

Introduce the minimum immutable domain model for a provisional thesis.

## Acceptance Criteria

- A thesis has its own generated `ThesisId`.
- A thesis records a non-blank statement.
- Original validated statement text is preserved.
- An explicit identity can be supplied during reconstruction.
- Two separately created theses receive distinct identities.
- No aggregate ownership, persistence, event, or application API changes.

## Out of Scope

- Attaching a thesis to an investigation.
- Linking hypotheses, claims, or interpretations.
- Thesis status, versioning, confidence, assessment, or invalidation.
- SQLite persistence and domain events.
- Automatic synthesis or AI integration.

## Architectural Notes

The initial thesis is immutable and domain-neutral. Ownership and grounding
rules must be earned by a later aggregate story rather than embedded
prematurely.
