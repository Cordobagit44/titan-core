# CORE-140 — Cover Assessment Workflow Acceptance

## Context

Assessment behavior now exists at domain, repository, event-store, and application
levels, but the composed acceptance workflow does not prove that `bootstrap()`
can create and reconstruct a narrative assessment across a real application
restart.

## Goal

Extend the persisted investigation workflow with narrative assessment creation
and reconstruction.

## Acceptance Criteria

- The composed application creates an assessment through `add_assessment`.
- The assessment references an existing thesis and is created before closure.
- Closing and recreating the application preserves assessment identity, thesis
  reference, narrative, and insertion order.
- Listing the reconstructed investigation preserves the same assessment state.
- Existing investigation, hypothesis, evidence, claim, interpretation, thesis,
  decision, and closure assertions remain intact.
- No production behavior, schema, API, or dependency changes.
- The complete quality gates pass.

## Out of Scope

- New assessment behavior or invariants.
- Verdicts, scores, confidence values, or automatic decisions.
- Direct inspection of internal repositories.
- Thesis selection, synthesis, HTTP, CLI, or AI integration.

## Architectural Notes

The acceptance test exercises only the public `TitanApplication` surface on
both sides of a real SQLite-backed restart.

## Validation

- Assessment-enabled acceptance workflow — passed
- pytest — 315 passed
- Ruff lint — passed
- Ruff format — passed
- mypy — passed
- GitHub Actions CI — passed
