# CORE-078 — Protect Evidence Addition on Closed Investigations

## Status

Done

## Context

TITAN Core already treated closed investigations as immutable for investigation
state changes such as adding or removing hypotheses and reactivation attempts.

Evidence addition bypassed that aggregate-level protection because the
`AddEvidence` application use case located a `Hypothesis` and called
`Hypothesis.add_evidence()` directly.

As a result, a closed investigation could still receive new evidence even
though the lifecycle rule says closed investigations prevent modifications
until reopened.

## Goal

Ensure evidence cannot be added while an investigation is closed and keep the
immutability rule inside the `Investigation` aggregate boundary.

## Domain Behavior

`Investigation.add_evidence()` now:

- rejects evidence addition when the investigation is `CLOSED` using
  `ValueError("investigation is closed")`;
- locates the target hypothesis by identifier;
- raises `LookupError("hypothesis not found")` when the target hypothesis does
  not exist;
- delegates the actual evidence attachment and `EvidenceAdded` emission to the
  target `Hypothesis`;
- returns the target hypothesis.

## Application Behavior

`AddEvidence` now routes mutation through `Investigation.add_evidence()` rather
than mutating the hypothesis directly.

Existing behavior remains unchanged for:

- evidence description validation;
- source validation;
- relationship validation;
- `UNSPECIFIED` rejection for new evidence;
- `EvidenceAdded` persistence;
- Unit of Work commit and rollback behavior.

Evidence addition against a closed investigation rolls back and propagates
`ValueError("investigation is closed")`.

## Acceptance Criteria

- A domain-level evidence addition succeeds for an open investigation.
- Adding evidence to a closed investigation raises `ValueError` with
  `investigation is closed`.
- Adding evidence for an unknown hypothesis raises `LookupError` with
  `hypothesis not found`.
- `AddEvidence` routes mutation through the `Investigation` aggregate.
- `AddEvidence` rolls back when the investigation is closed.
- Existing `EvidenceAdded` behavior remains unchanged.
- Existing persistence and relationship behavior remains unchanged.
- The complete test suite passes.
- Ruff passes.
- Ruff format check passes.
- mypy passes.

## Out of Scope

CORE-078 does not introduce:

- new investigation statuses;
- evidence removal or editing;
- evidence weighting or scoring;
- confidence or certainty;
- assessments;
- claims or interpretations;
- automatic hypothesis decisions;
- new domain events;
- persistence schema changes;
- CLI or HTTP APIs;
- AI integrations.

## Architectural Notes

Closed-investigation immutability is an aggregate invariant. The application
layer orchestrates the operation, while the `Investigation` aggregate owns the
rule that determines whether evidence mutation is allowed.

`Hypothesis` remains responsible for attaching evidence and emitting
`EvidenceAdded`. CORE-078 changes the mutation path, not the event definition or
persistence model.

## TDD Evidence

RED was established by adding domain tests for `Investigation.add_evidence()`
before the method existed. GitHub Actions failed in mypy with three
`attr-defined` errors for the missing aggregate operation.

GREEN was established after implementing the aggregate mutation path, routing
`AddEvidence` through it, and adding application rollback coverage for closed
investigations.

## Validation

- GitHub Actions CI passed.
- Ruff lint passed.
- Ruff format check passed.
- mypy passed on 62 source files.
- pytest — 151 passed.
- Existing persistence schema and domain event definitions were unchanged.
