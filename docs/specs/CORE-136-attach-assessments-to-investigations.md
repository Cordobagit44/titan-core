# CORE-136 — Attach Assessments to Investigations

## Context

CORE-135 introduces narrative assessments linked to a thesis, but assessments
have no owning aggregate. Investigations already own the theses and reasoning
state that an assessment evaluates.

## Goal

Allow open investigations to own narrative assessments for their existing theses.

## Acceptance Criteria

- An investigation exposes assessments as an immutable tuple.
- Draft and active investigations accept an assessment.
- The referenced thesis must belong to the investigation.
- Adding an assessment emits `AssessmentAdded` with investigation, assessment,
  and thesis IDs.
- Reusing an `AssessmentId` is rejected without mutation or event.
- Closed investigations reject assessment attachment.
- Equal narratives remain distinct when identities differ.
- No persistence or application API changes.
- The complete quality gates pass.

## Out of Scope

- Assessment revision, selection, replacement, removal, or status.
- Categorical verdicts, scoring, percentages, or confidence.
- SQLite and domain-event persistence.
- Reports, interfaces, automation, or AI synthesis.

## Architectural Notes

The investigation is the narrowest stable boundary that owns both the evaluated
thesis and its narrative assessment.
