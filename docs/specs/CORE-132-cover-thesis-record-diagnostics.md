# CORE-132 — Cover Thesis Record Diagnostics

## Context

CORE-128 reconstructs persisted theses through contextual UUID and required-text
validation, but those failure paths are not covered directly. A malformed thesis
row must fail explicitly rather than surface as an ambiguous parser or domain
error.

## Goal

Verify contextual diagnostics for malformed persisted thesis records.

## Acceptance Criteria

- An invalid persisted thesis ID reports a malformed thesis record and invalid ID.
- A blank persisted thesis statement reports the owning thesis ID and field name.
- Original parser or validation failures remain available through exception behavior.
- Valid thesis reconstruction remains unchanged.
- No schema, domain model, application API, or dependency changes.
- The complete quality gates pass.

## Out of Scope

- Schema repair or data correction.
- Thesis assessment, selection, removal, or versioning.
- Additional event-store diagnostics.

## Architectural Notes

Validation remains at the SQLite deserialization boundary. This story secures
existing behavior with focused regression coverage.
