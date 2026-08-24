# CORE-119 — Prevent Cross-Hypothesis Interpretation Reuse

## Goal

Preserve exclusive interpretation identity ownership while modifying an
investigation.

## Acceptance Criteria

- Attaching an interpretation whose identifier belongs to another hypothesis is
  rejected.
- The rejection occurs at the investigation aggregate boundary.
- The target hypothesis remains unchanged and emits no event after rejection.
- Interpretations with distinct identifiers remain governed by existing
  hypothesis rules.

## Architectural Notes

This story extends the aggregate identity ownership rules already applied to
evidence and claims. Hypothesis-level reference and duplicate validation remains
unchanged. No SQLite schema, application API, event payload, scoring, or AI
behavior is introduced.
