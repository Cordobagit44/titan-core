# CORE-053 — Emit Evidence Added Domain Event

## Status

Done

## Context

A `Hypothesis` owns a collection of evidence and already exposes
`add_evidence()` as the domain operation responsible for adding evidence to
that collection.

Before this story, adding evidence changed the state of the hypothesis but did
not produce a domain event describing that mutation.

Other meaningful hypothesis state transitions already emit domain events.
Confirming a hypothesis emits `HypothesisConfirmed`, and rejecting a hypothesis
emits `HypothesisRejected`.

Adding evidence is also a meaningful domain mutation and should be observable
through the same domain event mechanism.

## Goal

Emit an `EvidenceAdded` domain event whenever evidence is successfully added
to a hypothesis.

## Requirements

1. Introduce an `EvidenceAdded` domain event.
2. The event must preserve the `HypothesisId` of the hypothesis receiving the
   evidence.
3. The event must preserve the `EvidenceId` of the evidence being added.
4. `Hypothesis.add_evidence()` must continue adding the evidence to the
   hypothesis.
5. `Hypothesis.add_evidence()` must record exactly one `EvidenceAdded` event
   after the evidence is added.
6. `EvidenceAdded` must become part of the events that can be recorded by a
   `Hypothesis`.
7. Existing hypothesis confirmation and rejection behavior must remain
   unchanged.
8. This story must not introduce persistence or application-layer
   coordination for the new event.

## Domain Design

`Hypothesis` is responsible for recording `EvidenceAdded` because it owns the
evidence collection and performs the mutation.

The event identifies both sides of the domain change:

- the `HypothesisId` identifies the hypothesis that received the evidence;
- the `EvidenceId` identifies the evidence that was added.

The event does not require an `InvestigationId` because that information is not
part of the hypothesis-level mutation itself.

## Out of Scope

This story does not:

- persist `EvidenceAdded` through `DomainEventRepository`;
- add SQLite support for `EvidenceAdded`;
- modify the `AddEvidence` application use case to persist domain events;
- introduce a Unit of Work;
- introduce an Event Bus;
- introduce an Outbox;
- introduce transaction coordination;
- change the existing investigation persistence model.

Those concerns can be addressed by subsequent stories.

## Acceptance Criteria

- Adding evidence still stores the evidence on the hypothesis.
- Adding evidence emits exactly one `EvidenceAdded` domain event.
- The emitted event contains the original `HypothesisId`.
- The emitted event contains the original `EvidenceId`.
- Existing hypothesis behavior remains valid.
- The complete test suite passes.
- Ruff passes.
- mypy passes.

## Validation

Validated with:

- `uv run pytest` — 107 passed
- `uv run ruff check .` — passed
- `uv run mypy src` — passed with no issues in 27 source files
