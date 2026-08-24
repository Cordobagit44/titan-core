# CORE-100 — Validate Persisted Record Text

## Status

Done

## Context

The domain requires non-blank investigation titles and purposes, hypothesis
statements, and evidence descriptions and sources. SQLite restoration currently
accepts blank investigation text and exposes context-free domain errors for
blank nested text.

## Goal

Reject blank required text at the SQLite deserialization boundary with
consistent record and field context.

## Acceptance Criteria

- Valid persisted records continue to reconstruct normally.
- Blank persisted investigation titles and purposes are rejected.
- Blank persisted hypothesis statements are rejected.
- Blank persisted evidence descriptions and sources are rejected.
- Each error identifies the record type, identifier, and invalid field.
- Existing persistence, ordering, migration, and restoration remain unchanged.
- No public signature, schema, or dependency changes.
- The complete test suite and quality gates pass.

## Out of Scope

- Trimming or rewriting persisted text.
- Minimum or maximum text lengths.
- Content normalization or semantic duplicate detection.
- Changing database constraints or schemas.

## Architectural Notes

Required-text validation is performed at the SQLite deserialization boundary
before reconstructed values reach aggregate and entity restoration.

## Validation

- Targeted SQLite investigation repository tests — 24 passed
- pytest — 204 passed
- Ruff lint — passed
- Ruff format — 180 files already formatted
- mypy — 65 source files checked
