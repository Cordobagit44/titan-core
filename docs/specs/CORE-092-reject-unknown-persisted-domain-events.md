# CORE-092 — Reject Unknown Persisted Domain Events

## Status

Done

## Context

`SqliteDomainEventRepository.list_all()` reconstructs recognized event types
through an explicit conditional chain. A row with an unknown `event_type` is
currently skipped without an error, causing callers to receive an incomplete
history with no indication that a persisted event was omitted.

## Goal

Protect historical traceability by failing explicitly when the event store
contains an unsupported event type.

## Acceptance Criteria

- All currently supported event types continue to reconstruct normally.
- Reading an unknown persisted event type raises a `ValueError` identifying the
  event type.
- Unknown event rows are not silently omitted.
- Event ordering and persistence behavior remain unchanged.
- No public method signature, schema, event type, or dependency changes.
- The complete test suite and quality gates pass.

## Out of Scope

- Dynamically registering event deserializers.
- Ignoring or quarantining unknown events.
- Recovering malformed payload values.
- Changing migration behavior.

## Architectural Notes

The repository owns deserialization and therefore owns the explicit failure for
an event type it cannot reconstruct.

## Validation

- Targeted SQLite domain-event repository tests — 13 passed
- pytest — 180 passed
- Ruff lint — passed
- Ruff format — 172 files already formatted
- mypy — 65 source files checked
