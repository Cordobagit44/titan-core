# CORE-093 — Validate Persisted Domain Event Payloads

## Status

Done

## Context

CORE-092 rejects unknown persisted event types explicitly. Recognized event
types can still contain `NULL` in fields required for reconstruction. The
repository currently passes those values directly to UUID or datetime parsing,
producing low-level exceptions that do not identify the corrupt event payload.

## Goal

Validate required payload fields before reconstructing a recognized persisted
domain event and report the event type and missing field explicitly.

## Acceptance Criteria

- Supported events with complete payloads continue to reconstruct normally.
- A missing required payload field raises `ValueError`.
- The error identifies both the persisted event type and missing field.
- Investigation, closure, hypothesis, and evidence payload shapes are covered.
- Event ordering, saving, migration, and unknown-type behavior remain unchanged.
- No public method signature, schema, event type, or dependency changes.
- The complete test suite and quality gates pass.

## Out of Scope

- Recovering or inventing missing payload values.
- Validating malformed non-null UUID or datetime text beyond existing parsers.
- Dynamically registering event deserializers.
- Changing database constraints.

## Architectural Notes

Payload validation remains private to the SQLite repository's deserialization
boundary. It runs immediately before converting a required stored value.

## Validation

- Targeted SQLite domain-event repository tests — 17 passed
- pytest — 184 passed
- Ruff lint — passed
- Ruff format — 173 files already formatted
- mypy — 65 source files checked
