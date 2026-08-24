# CORE-128 — Persist Investigation Theses

## Context

CORE-127 makes provisional theses part of the investigation aggregate, but the
SQLite investigation repository does not store them. Saving and reconstructing
an investigation therefore loses its theses.

## Goal

Persist and restore investigation-owned theses as SQLite aggregate state.

## Acceptance Criteria

- Repository initialization creates a `theses` table when absent.
- Saving an investigation stores thesis identity, investigation owner, and statement.
- `get()` restores theses in insertion order with original identities and text.
- `list()` restores the same thesis state.
- Reconstruction leaves no pending `ThesisAdded` events.
- Re-saving an investigation replaces its prior thesis rows safely.
- Existing databases initialize safely without a thesis migration step.
- Existing aggregate persistence remains unchanged.
- The complete quality gates pass.

## Out of Scope

- Persisting `ThesisAdded` in the domain-event repository.
- Application use cases or bootstrap changes.
- Thesis removal, selection, status, grounding, assessment, or versioning.
- Specialized malformed-thesis diagnostics beyond current domain validation.

## Architectural Notes

Theses are stored directly beneath their owning investigation. Repository
reconstruction supplies them to the aggregate restore path without replaying
mutation events.
