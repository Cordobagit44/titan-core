# CORE-116 — Cover Interpretation Workflow Acceptance

## Goal

Verify that the composed SQLite-backed application preserves an explicit
interpretation across an application restart.

## Acceptance Criteria

- The acceptance workflow creates an interpretation through
  `TitanApplication.add_interpretation`.
- The application is closed and reconstructed against the same SQLite database.
- The restored hypothesis contains the original interpretation identity,
  rationale, claim reference, and hypothesis reference.
- Existing investigation, hypothesis, evidence, claim, decision, and closure
  assertions remain intact.

## Architectural Notes

This story adds end-to-end confidence for behavior already implemented through
CORE-115. It introduces no new production API, domain rule, schema, dependency,
automatic reasoning, or AI integration.
