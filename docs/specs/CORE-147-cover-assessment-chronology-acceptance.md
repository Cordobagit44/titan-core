# CORE-147 — Cover Assessment Chronology Acceptance

## Context

Assessment timestamps are covered at domain and SQLite boundaries, but the
composed application workflow does not explicitly prove that the timestamp
returned by `add_assessment` survives application shutdown and reconstruction.

## Goal

Extend the public acceptance workflow with exact assessment timestamp
preservation.

## Acceptance Criteria

- The assessment created through `TitanApplication.add_assessment` exposes a
  timezone-aware timestamp.
- Restarting the SQLite-backed application preserves the exact timestamp.
- Listing the reconstructed investigation preserves the same assessment state.
- Existing workflow assertions remain intact.
- No production behavior, schema, API, or dependency changes.
- The complete quality gates pass.

## Out of Scope

- Direct repository or event-store inspection.
- User-supplied timestamps through the application API.
- Verdicts, scores, confidence values, or automatic decisions.

## Validation

- Assessment chronology acceptance workflow — passed
- pytest — 330 passed
- Ruff lint — passed
- Ruff format — passed
- mypy — passed
- GitHub Actions CI — passed
