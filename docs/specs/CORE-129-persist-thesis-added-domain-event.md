# CORE-129 — Persist ThesisAdded Domain Event

## Context

CORE-127 emits `ThesisAdded`, while CORE-128 persists thesis aggregate state.
The SQLite domain-event repository still rejects the event, leaving successful
thesis attachment absent from durable history.

## Goal

Persist and reconstruct `ThesisAdded` with investigation and thesis identity.

## Acceptance Criteria

- The event schema includes nullable `thesis_id` storage.
- Existing event tables migrate without losing earlier rows.
- Saving `ThesisAdded` preserves investigation and thesis IDs.
- `list_all()` reconstructs the original event in order.
- Missing required fields are rejected with event and field context.
- Malformed identifiers are rejected with event and field context.
- Existing event types, migrations, ordering, and diagnostics remain intact.
- The complete quality gates pass.

## Out of Scope

- Application orchestration or bootstrap changes.
- Thesis content in the event payload.
- Event replay, event bus, outbox, removal, or update events.

## Architectural Notes

The event store records the identity transition, while aggregate persistence
remains the source of the thesis statement.

## Validation

- Thesis event persistence tests — 4 passed
- pytest — 284 passed
- Ruff lint — passed
- Ruff format — passed
- mypy — passed
- GitHub Actions CI — passed
