# CORE-123 — Validate Persisted Reasoning Text

## Goal

Reject blank required claim and interpretation text at the SQLite
deserialization boundary with consistent record and field context.

## Acceptance Criteria

- Valid persisted claims and interpretations continue to reconstruct normally.
- Blank persisted claim statements are rejected.
- Blank persisted interpretation rationales are rejected.
- Each error identifies the record type, identifier, and invalid field.
- Existing persistence, ordering, restoration, and ownership behavior remains
  unchanged.

## Out of Scope

- Trimming or rewriting persisted text.
- Minimum or maximum text lengths.
- Content normalization or semantic validation.
- Changing database constraints or schemas.

## Architectural Notes

The existing required-text validation boundary is extended to the richer
reasoning records introduced after CORE-100. No public API, schema, event,
scoring, or AI behavior is introduced.
