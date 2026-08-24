# CORE-120 — Reject Restored Interpretation Reuse

## Goal

Apply exclusive interpretation identity ownership when reconstructing an
investigation.

## Acceptance Criteria

- Restoring hypotheses that reuse one interpretation identifier is rejected.
- The rejection uses the established cross-hypothesis ownership error.
- Interpretations with distinct identifiers remain restorable.
- Existing hypothesis, evidence, claim, and interpretation state remains
  unchanged when valid.

## Architectural Notes

Restoration must enforce the same aggregate identity ownership established for
live interpretation attachment in CORE-119. SQLite behavior remains unchanged
because interpretation identifiers are already primary keys. No API, schema,
event, scoring, or AI behavior is introduced.
