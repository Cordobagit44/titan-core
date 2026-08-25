# CORE-138 — Persist AssessmentAdded Domain Event

## Context

CORE-136 emits `AssessmentAdded`, while CORE-137 persists assessment aggregate
state. The SQLite event repository still rejects the event.

## Goal

Persist and reconstruct `AssessmentAdded` with investigation, assessment, and thesis identity.

## Acceptance Criteria

- The event schema includes nullable `assessment_id` storage.
- Existing event tables migrate without losing rows.
- Saving preserves investigation, assessment, and thesis IDs.
- `list_all()` reconstructs the original event in order.
- Missing fields and malformed identifiers receive contextual diagnostics.
- Existing event behavior and migrations remain intact.
- The complete quality gates pass.

## Out of Scope

- Application orchestration or bootstrap changes.
- Assessment narrative in event payloads.
- Verdicts, scores, event replay, bus, or outbox.

## Architectural Notes

Event history records identity transitions; aggregate persistence remains the
source of narrative assessment content.
