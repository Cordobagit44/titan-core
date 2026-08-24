# CORE-087 — Protect Decided Hypotheses from Evidence Addition

## Status

Done

## Context

Confirmation and rejection are terminal hypothesis decisions. Although
CORE-086 preserves decided hypotheses inside their investigation, a confirmed
or rejected hypothesis still accepts new evidence. That changes the recorded
evidence basis after the decision and emits a new `EvidenceAdded` event without
a corresponding new decision.

## Goal

Preserve the historical basis of terminal decisions by allowing evidence to be
added only while a hypothesis is pending.

## Acceptance Criteria

- A pending hypothesis continues to accept evidence.
- A confirmed hypothesis rejects new evidence.
- A rejected hypothesis rejects new evidence.
- A failed addition leaves the evidence collection unchanged.
- A failed addition emits no `EvidenceAdded` event.
- The application use case rolls back and does not commit after a failed
  addition.
- Existing closed-investigation protection remains unchanged.
- The complete test suite and quality gates pass.

## Out of Scope

- Reopening or reversing hypothesis decisions.
- Editing or deleting existing evidence.
- Evidence weighting, scores, or confidence.
- New event types or persistence schema changes.

## Architectural Notes

The invariant belongs to `Hypothesis`, which owns both its decision status and
its evidence collection. The `Investigation` aggregate continues to enforce
investigation lifecycle protections.

## Validation

- Targeted hypothesis and evidence-addition tests — 30 passed
- pytest — 174 passed
- Ruff lint — passed
- Ruff format — 167 files already formatted
- mypy — 65 source files checked
