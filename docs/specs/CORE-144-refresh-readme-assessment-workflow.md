# CORE-144 — Refresh README for Assessment Workflow

## Context

The public README documents the reasoning flow through provisional theses but
does not yet show the implemented narrative assessment model, application use
case, SQLite restoration, or current validated suite size.

## Goal

Bring the public project overview and usage example into alignment with the
implemented assessment workflow.

## Acceptance Criteria

- Implemented capabilities mention investigation-owned narrative assessments.
- The domain and persistence summaries include assessments.
- The usage example creates an assessment for a provisional thesis before
  closing the investigation.
- The reconstruction description includes assessments.
- The application use-case list includes `add_assessment`.
- The documented passing test count matches the validated suite.
- The README does not imply verdicts, scores, confidence values, or automatic
  investment decisions.
- No production behavior, schema, API, or dependency changes.
- The complete quality gates pass.

## Out of Scope

- New assessment behavior.
- Investment recommendations or portfolio decisions.
- HTTP, CLI, UI, or AI integration.

## Validation

- README assessment workflow review — passed
- pytest — 321 passed
- Ruff lint — passed
- Ruff format — passed
- mypy — passed
- GitHub Actions CI — passed
