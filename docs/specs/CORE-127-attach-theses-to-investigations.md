# CORE-127 — Attach Theses to Investigations

## Context

CORE-126 introduces a provisional `Thesis`, but it has no owning reasoning
boundary. An investigation is the aggregate that contains the hypotheses,
evidence, claims, and interpretations from which a thesis is formed.

## Goal

Allow open investigations to own provisional theses.

## Acceptance Criteria

- An investigation exposes theses as an immutable tuple.
- A draft or active investigation accepts a thesis.
- Adding a thesis emits `ThesisAdded` with investigation and thesis IDs.
- Reusing a `ThesisId` in one investigation is rejected without mutation or
  event.
- A closed investigation cannot accept theses.
- Equal statements do not collapse distinct thesis identities.
- No persistence or application API changes.

## Out of Scope

- Thesis removal, replacement, status, versioning, or selection.
- Explicit links to hypotheses, claims, or interpretations.
- SQLite and domain-event persistence.
- Confidence, assessment, invalidation, scoring, or AI synthesis.

## Architectural Notes

The investigation is the narrowest stable aggregate boundary for a provisional
conclusion. Multiple distinct identities remain possible without prematurely
defining current-versus-historical thesis semantics.
