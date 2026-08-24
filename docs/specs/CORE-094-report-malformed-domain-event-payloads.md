# CORE-094 — Report Malformed Domain Event Payloads

## Status

Done

## Context

CORE-093 identifies required event fields stored as `NULL`. Required UUID and
datetime fields that are present but malformed still raise parser-specific
errors without identifying the persisted event type or payload field.

## Goal

Report malformed UUID and datetime payload values with explicit event and field
context while retaining the original parser exception as the cause.

## Acceptance Criteria

- Valid persisted event payloads continue to reconstruct normally.
- A malformed investigation identifier raises a contextual `ValueError`.
- A malformed hypothesis identifier raises a contextual `ValueError`.
- A malformed evidence identifier raises a contextual `ValueError`.
- A malformed closure timestamp raises a contextual `ValueError`.
- The error identifies both event type and malformed field.
- Missing-field, unknown-type, ordering, saving, and migration behavior remain
  unchanged.
- No public signature, schema, event type, or dependency changes.
- The complete test suite and quality gates pass.

## Out of Scope

- Repairing malformed values.
- Validating payload semantics beyond UUID and ISO datetime parsing.
- Changing database constraints.
- Dynamically registering event deserializers.

## Architectural Notes

Private repository parsing helpers translate low-level parser failures at the
SQLite deserialization boundary and preserve exception chaining.

## Validation

- Targeted SQLite domain-event repository tests — 21 passed
- pytest — 188 passed
- Ruff lint — passed
- Ruff format — 174 files already formatted
- mypy — 65 source files checked
