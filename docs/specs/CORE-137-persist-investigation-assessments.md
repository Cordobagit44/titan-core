# CORE-137 — Persist Investigation Assessments

## Context

CORE-136 makes narrative assessments part of the investigation aggregate, but
the SQLite investigation repository does not store them. Saving and restoring
an investigation therefore loses its assessments.

## Goal

Persist and reconstruct investigation-owned narrative assessments.

## Acceptance Criteria

- Repository initialization creates an `assessments` table when absent.
- Saving stores assessment identity, investigation owner, thesis reference, and narrative.
- `get()` and `list()` restore assessments in insertion order.
- Original identities, thesis references, and narratives survive reconstruction.
- Reconstruction leaves no pending `AssessmentAdded` events.
- Re-saving replaces prior assessment rows safely.
- Restoration rejects assessment references to theses outside the investigation.
- Existing aggregate persistence remains unchanged.
- The complete quality gates pass.

## Out of Scope

- `AssessmentAdded` event-store persistence.
- Application orchestration or bootstrap changes.
- Verdicts, scores, percentages, selection, revision, or removal.
- Specialized malformed-assessment diagnostics.

## Architectural Notes

Assessments are stored directly beneath their investigation and reconstructed
after theses so the aggregate reference invariant remains authoritative.

## Validation

- Assessment persistence tests — 3 passed
- pytest — 307 passed
- Ruff lint — passed
- Ruff format — passed
- mypy — passed
- GitHub Actions CI — passed
