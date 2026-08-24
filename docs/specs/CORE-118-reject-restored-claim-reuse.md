# CORE-118 — Reject Restored Claim Reuse

## Goal

Apply exclusive claim identity ownership when reconstructing an investigation.

## Acceptance Criteria

- Restoring hypotheses that reuse one claim identifier is rejected.
- The rejection uses the established cross-hypothesis ownership error.
- Claims with distinct identifiers remain restorable.
- Existing hypothesis, evidence, claim, and interpretation state remains
  unchanged when valid.

## Architectural Notes

Restoration must enforce the same aggregate identity ownership established for
live claim attachment in CORE-117. SQLite behavior remains unchanged because
claim identifiers are already primary keys. No API, schema, event, scoring, or
AI behavior is introduced.
