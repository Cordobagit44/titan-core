# CORE-131 — Cover Thesis Workflow Acceptance

## Context

Thesis behavior now exists at domain, repository, event-store, and application
levels, but the composed acceptance workflow does not prove that `bootstrap()`
can create and reconstruct a thesis across a real application restart.

## Goal

Extend the persisted investigation workflow with provisional thesis creation
and reconstruction.

## Acceptance Criteria

- The composed application creates a thesis through `add_thesis`.
- Creation occurs before investigation closure.
- Closing and recreating the application preserves thesis identity and statement.
- Listing the reconstructed investigation preserves the same thesis state.
- Existing investigation, hypothesis, evidence, claim, interpretation,
  decision, and closure assertions remain intact.
- No production behavior, schema, API, or dependency changes.
- The complete quality gates pass.

## Out of Scope

- New thesis behavior or invariants.
- Direct inspection of internal repositories.
- Selection, assessment, synthesis, HTTP, CLI, or AI integration.

## Architectural Notes

The acceptance test exercises only the public `TitanApplication` surface on
both sides of a real SQLite-backed restart.

## Validation

- Thesis-enabled acceptance workflow — passed
- pytest — 288 passed
- Ruff lint — passed
- Ruff format — passed
- mypy — passed
- GitHub Actions CI — passed
