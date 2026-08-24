# CORE-109 — Cover Claim Workflow Acceptance

## Status

Done

## Context

Claim behavior is covered at domain, application, and repository levels, but
the composed acceptance workflow does not prove that `bootstrap()` can create a
claim and reconstruct it after an application restart.

## Goal

Extend the complete persisted investigation workflow with evidence-grounded
claim creation and reconstruction.

## Acceptance Criteria

- The composed application creates a claim through `add_claim`.
- The claim is created before hypothesis decision and investigation closure.
- Closing and recreating the application preserves claim identity.
- Restored statement and evidence provenance match the created claim.
- The surrounding investigation, hypothesis, and evidence workflow remains
  unchanged.
- No production behavior, schema, API, or dependency changes.
- The complete test suite and quality gates pass.

## Out of Scope

- New claim behavior or invariants.
- Direct inspection of internal repositories from the acceptance test.
- HTTP, CLI, automatic extraction, or AI integration.

## Architectural Notes

The acceptance test exercises the public `TitanApplication` surface on both
sides of a real SQLite-backed application restart.

## Validation

- Claim-enabled acceptance workflow — 1 passed
- pytest — 232 passed
- Ruff lint — passed
- Ruff format — 195 files already formatted
- mypy — 71 source files checked
