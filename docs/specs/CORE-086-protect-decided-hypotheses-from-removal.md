# CORE-086 — Protect Decided Hypotheses from Removal

## Status

Done

## Context

CORE-085 made hypothesis confirmation and rejection terminal, non-repeatable
decisions. An open investigation can still remove a confirmed or rejected
hypothesis, however, which removes the decided hypothesis from the aggregate
even though its decision event remains part of the historical record.

## Goal

Preserve terminal hypothesis decisions by allowing only pending hypotheses to
be removed from an investigation.

## Acceptance Criteria

- A pending hypothesis can still be removed.
- A confirmed hypothesis cannot be removed.
- A rejected hypothesis cannot be removed.
- A failed removal leaves the hypothesis in the investigation.
- A failed removal emits no `HypothesisRemoved` event.
- The application use case rolls back and does not commit after a failed
  removal.
- Existing closed-investigation protection remains unchanged.
- The complete test suite and quality gates pass.

## Out of Scope

- Reversing a hypothesis decision.
- Archiving hypotheses.
- Deleting evidence independently.
- New event types or persistence schema changes.
- Automatic decisions, scores, confidence, claims, or assessments.

## Architectural Notes

The invariant belongs to the `Investigation` aggregate because removal changes
aggregate membership. `Hypothesis` remains responsible for its own decision
transitions.

## Validation

- Targeted hypothesis-removal tests — 13 passed
- pytest — 170 passed
- Ruff lint — passed
- Ruff format — 166 files already formatted
- mypy — 65 source files checked
