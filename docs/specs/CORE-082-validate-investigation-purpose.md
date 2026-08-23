# CORE-082 — Validate Investigation Purpose

## Status

Done

## Context

An investigation is a persistent unit of work created to reduce uncertainty about a defined question or thesis. The current domain requires a non-empty title but accepts an empty or whitespace-only `purpose`.

That allows an investigation to be created without recording why it exists, even though purpose is already part of the aggregate and is persisted by the application.

## Goal

Require every newly created investigation to have a non-empty purpose.

## Domain Behavior

`Investigation.create()` must reject an empty or whitespace-only purpose with:

`ValueError("purpose must not be empty")`

Valid purposes continue to be stored unchanged.

Restoration of already persisted investigations is outside this validation change. CORE-082 must not introduce a migration or rewrite historical data.

## Application Behavior

`CreateInvestigation` continues to delegate creation rules to the domain.

If purpose validation fails, the existing Unit of Work error path must roll back and must not commit.

## Acceptance Criteria

- `Investigation.create()` rejects an empty purpose.
- `Investigation.create()` rejects a whitespace-only purpose.
- A valid purpose is preserved unchanged.
- `CreateInvestigation` propagates purpose validation failure.
- A failed application creation does not commit and rolls back the Unit of Work.
- Existing investigation lifecycle, hypothesis, evidence, persistence, and domain-event behavior remain unchanged.
- The complete test suite passes.
- Ruff lint passes.
- Ruff format check passes.
- mypy passes.

## Out of Scope

CORE-082 does not introduce:

- purpose editing;
- purpose length limits;
- title normalization;
- purpose normalization;
- thesis modeling;
- claims or interpretations;
- assessments;
- evidence weighting;
- confidence or certainty scoring;
- CLI or HTTP APIs;
- AI integrations.

## Architectural Notes

Purpose is already authoritative investigation state. Validating it at aggregate creation keeps the invariant in the domain rather than duplicating it in application or persistence code.

The story adds the smallest demonstrated invariant and does not introduce a new abstraction.
