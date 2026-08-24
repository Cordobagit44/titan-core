# CORE-113 — Persist Investigation Interpretations

## Goal

Preserve interpretations when an investigation aggregate is saved to and
restored from SQLite.

## Acceptance Criteria

- SQLite stores each interpretation identity, owning hypothesis, source claim,
  and rationale.
- `get()` and `list()` restore interpretations after their claims.
- Aggregate reconstruction does not leave pending domain events.
- Saving an aggregate replaces its prior interpretation rows safely.
- The application API remains unchanged.

## Architectural Notes

Interpretations remain part of the hypothesis-owned aggregate. The repository
persists their state without weakening domain validation during reconstruction.
