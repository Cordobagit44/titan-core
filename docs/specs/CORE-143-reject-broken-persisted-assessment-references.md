# CORE-143 — Reject Broken Persisted Assessment References

## Context

Assessment reconstruction parses thesis references correctly, but a
well-formed UUID that does not identify a thesis owned by the investigation is
currently reported only as a generic aggregate error. Persistence corruption
should identify the damaged assessment record.

## Goal

Report a contextual diagnostic when a persisted assessment references a thesis
that its investigation does not own.

## Acceptance Criteria

- SQLite reconstruction rejects an assessment whose well-formed `thesis_id`
  does not identify an owned persisted thesis.
- The error identifies the assessment and reports that its thesis was not found.
- Valid assessment reconstruction remains unchanged.
- Aggregate restoration invariants remain authoritative.
- No schema, application API, domain event, or dependency changes.
- The complete quality gates pass.

## Out of Scope

- Cross-investigation repair or automatic deletion.
- Database foreign-key migration.
- Verdicts, scores, confidence values, or automatic decisions.
- HTTP, CLI, or AI integration.

## Architectural Notes

The SQLite mapper translates the aggregate's missing-thesis invariant into a
record-specific persistence diagnostic before constructing the investigation.

## Validation

Pending implementation and CI.
