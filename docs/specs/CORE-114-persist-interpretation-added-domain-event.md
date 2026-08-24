# CORE-114 — Persist InterpretationAdded Domain Event

## Goal

Preserve successful interpretation attachment in the SQLite domain-event
history.

## Acceptance Criteria

- `InterpretationAdded` is accepted by the SQLite event repository.
- Hypothesis, interpretation, and claim identifiers survive save and restore.
- Existing event tables migrate without losing earlier events.
- Missing required fields are rejected with event and field context.
- Malformed identifiers are rejected with event and field context.

## Architectural Notes

The event store records interpretation identity and lineage, not interpretation
rationale. Aggregate state remains the source for the full interpretation.
