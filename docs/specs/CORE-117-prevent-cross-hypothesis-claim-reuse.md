# CORE-117 — Prevent Cross-Hypothesis Claim Reuse

## Goal

Preserve exclusive claim identity ownership inside an investigation.

## Acceptance Criteria

- A claim identifier already owned by one hypothesis cannot be attached to
  another hypothesis in the same investigation.
- Rejection occurs before the target hypothesis mutates or emits an event.
- Distinct claim identifiers remain valid even when their statements match.
- Existing hypothesis-level claim validation remains unchanged.

## Architectural Notes

Claim identity ownership is an aggregate invariant because an investigation
coordinates multiple hypotheses. This story does not change persistence,
restoration, application APIs, event payloads, scoring, or AI behavior.
