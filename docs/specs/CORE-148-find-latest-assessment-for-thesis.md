# CORE-148 — Find Latest Assessment for Thesis

## Context

An investigation may preserve multiple narrative assessments for one thesis as
research evolves. Consumers currently must inspect the whole collection to
determine which evaluation is chronologically current.

## Goal

Let the investigation return the most recently recorded assessment for an
owned thesis.

## Acceptance Criteria

- `latest_assessment_for(thesis_id)` returns the assessment with the greatest
  `recorded_at` value.
- It returns `None` when the owned thesis has no assessments.
- It rejects an unknown thesis reference.
- If timestamps are equal, the most recently attached assessment wins
  deterministically.
- The query does not emit domain events or mutate aggregate state.
- Closed investigations allow the read-only query.
- No score, verdict, confidence value, or automatic decision is introduced.
- The complete quality gates pass.

## Out of Scope

- Application-layer exposure.
- Assessment editing, deletion, or supersession events.
- Persistence query optimization.
- HTTP, CLI, UI, or AI integration.

## Architectural Notes

The aggregate owns both theses and their assessment chronology, so it remains
the authority for resolving the latest narrative evaluation.

## Validation

Pending implementation and CI.
