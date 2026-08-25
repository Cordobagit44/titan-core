# CORE-135 — Introduce Narrative Assessment

## Context

TITAN now preserves a complete provisional thesis workflow, but it has no
explicit structure for evaluating a thesis. The accepted product direction is
to begin with explainable narrative assessment rather than a categorical
verdict or potentially misleading numeric confidence.

## Goal

Introduce the minimum immutable domain model for a narrative assessment linked
to a provisional thesis.

## Acceptance Criteria

- `AssessmentId` is an immutable UUID-backed identity with a factory.
- `Assessment` is immutable and owns an `AssessmentId`.
- Every assessment references one `ThesisId`.
- Every assessment contains a non-blank narrative.
- Explicit identities support deterministic reconstruction.
- Equal narratives remain distinct when identities differ.
- No aggregate ownership, persistence, event, or application changes.
- No categorical verdict or numeric confidence is introduced.
- The complete quality gates pass.

## Out of Scope

- Attaching assessments to investigations or theses.
- Assessment revision, selection, replacement, removal, or status.
- Persistence, domain events, application use cases, reports, or interfaces.
- Scoring, percentages, recommendation labels, automation, or AI synthesis.

## Architectural Notes

The narrative records explainable evaluation while `ThesisId` provides the
minimum explicit subject reference. Ownership and lifecycle semantics remain
for later focused stories.

## Validation

- Assessment domain tests — 5 passed
- pytest — 297 passed
- Ruff lint — passed
- Ruff format — passed
- mypy — passed
- GitHub Actions CI — passed
