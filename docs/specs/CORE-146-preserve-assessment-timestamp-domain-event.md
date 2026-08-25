# CORE-146 — Preserve Assessment Timestamp in Domain Event

## Context

Assessments now record when their narrative evaluation was formulated, but the
persisted `AssessmentAdded` fact carries only identities. Historical event
inspection should preserve the same time anchor as aggregate state.

## Goal

Include the assessment's immutable `recorded_at` timestamp in
`AssessmentAdded` and preserve it through the SQLite event store.

## Acceptance Criteria

- `AssessmentAdded` contains the exact assessment `recorded_at` value.
- SQLite saves and reconstructs the event timestamp.
- The event schema migrates older rows safely with an explicit Unix-epoch
  legacy marker for historical `AssessmentAdded` events.
- Missing or malformed event timestamps produce contextual diagnostics.
- Other event types and schemas remain behaviorally unchanged.
- The complete quality gates pass.

## Out of Scope

- Event sourcing.
- Assessment narrative duplication in the event payload.
- Verdicts, scores, confidence values, or automatic decisions.
- HTTP, CLI, UI, or AI integration.

## Validation

Pending implementation and CI.
