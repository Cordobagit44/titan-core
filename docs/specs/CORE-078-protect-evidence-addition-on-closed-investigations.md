# CORE-078 — Protect Evidence Addition on Closed Investigations

## Status

In Progress

## Context

TITAN Core already treats closed investigations as immutable for investigation
state changes such as adding or removing hypotheses and reactivation attempts.

Evidence addition currently bypasses that aggregate-level protection because
the `AddEvidence` application use case locates a `Hypothesis` and calls
`Hypothesis.add_evidence()` directly.

As a result, a closed investigation can still receive new evidence even though
the documented lifecycle rule says closed investigations prevent modifications
until reopened.

## Goal

Ensure evidence cannot be added while an investigation is closed and keep the
immutability rule inside the `Investigation` aggregate boundary.

## Domain Behavior

Introduce an `Investigation.add_evidence()` operation that:

- rejects evidence addition when the investigation is `CLOSED` using
  `ValueError("investigation is closed")`;
- locates the target hypothesis by identifier;
- raises `LookupError("hypothesis not found")` when the target hypothesis does
  not exist;
- delegates the actual evidence attachment and `EvidenceAdded` emission to the
  target `Hypothesis`;
- returns the target hypothesis so the application layer can persist its pending
  domain events without bypassing the aggregate mutation boundary.

## Application Behavior

`AddEvidence` must use `Investigation.add_evidence()` rather than mutating the
hypothesis directly.

Existing behavior remains unchanged for:

- evidence description validation;
- source validation;
- relationship validation;
- `UNSPECIFIED` rejection for new evidence;
- `EvidenceAdded` persistence;
- Unit of Work commit and rollback behavior.

When evidence addition is attempted against a closed investigation, the use
case must roll back and propagate `ValueError("investigation is closed")`.

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
layer should orchestrate the operation, but the `Investigation` aggregate must
own the rule that determines whether evidence mutation is allowed.

`Hypothesis` remains responsible for attaching evidence and emitting
`EvidenceAdded`. CORE-078 changes the mutation path, not the event definition or
persistence model.
