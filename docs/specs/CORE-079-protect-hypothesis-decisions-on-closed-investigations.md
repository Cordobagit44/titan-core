# CORE-079 — Protect Hypothesis Decisions on Closed Investigations

## Status

Done

## Context

CORE-078 established that evidence mutation belongs behind the `Investigation`
aggregate boundary so a closed investigation cannot be changed indirectly
through one of its hypotheses.

The confirm and reject application use cases still located a hypothesis and
called `Hypothesis.confirm()` or `Hypothesis.reject()` directly. This allowed
hypothesis status to change after the owning investigation had been closed.

That behavior conflicted with the existing aggregate rule that closed
investigations prevent modifications until reopened.

## Goal

Ensure hypothesis decisions are protected by the owning `Investigation`
aggregate lifecycle.

Confirming or rejecting a hypothesis through the application layer must fail
while the investigation is closed and succeed again after it is reopened.

## Domain Model

Aggregate-level operations locate the requested hypothesis and delegate the
actual status transition to the `Hypothesis` entity.

The `Investigation` aggregate:

- rejects confirmation while closed;
- rejects rejection while closed;
- preserves existing hypothesis lookup errors;
- preserves the existing `HypothesisConfirmed` and `HypothesisRejected` events;
- allows the operations after reopening.

`Hypothesis` remains responsible for its own status transition invariants, such
as preventing confirmation of a rejected hypothesis and rejection of a
confirmed hypothesis.

## Application Behavior

`ConfirmHypothesis` and `RejectHypothesis` route their mutations through the
`Investigation` aggregate instead of mutating the located hypothesis directly.

The existing Unit of Work behavior remains unchanged:

- successful mutations save the investigation, persist the hypothesis event,
  and commit;
- rejected mutations roll back and re-raise the domain error.

## Persistence

No persistence schema changes are required.

Existing investigation and hypothesis status persistence remains unchanged.

## Domain Events

No new event types are introduced.

Successful confirmation continues to emit `HypothesisConfirmed` and successful
rejection continues to emit `HypothesisRejected` from the `Hypothesis` entity.
A rejected mutation on a closed investigation emits neither event.

## Acceptance Criteria

- A closed investigation rejects hypothesis confirmation.
- A closed investigation rejects hypothesis rejection.
- A reopened investigation allows hypothesis confirmation.
- A reopened investigation allows hypothesis rejection.
- Existing hypothesis status transition invariants remain unchanged.
- Existing hypothesis status domain events remain unchanged.
- `ConfirmHypothesis` rolls back when the aggregate rejects a closed mutation.
- `RejectHypothesis` rolls back when the aggregate rejects a closed mutation.
- Successful application behavior continues to commit and persist events.
- No SQLite schema change is introduced.
- The complete test suite passes.
- Ruff lint and format checks pass.
- mypy passes.

## Validation

- TDD red state captured in CI before production changes.
- pytest — 159 passed.
- Ruff lint — passed.
- Ruff format — passed.
- mypy — 64 source files checked successfully.

## Out of Scope

CORE-079 does not introduce:

- new hypothesis statuses;
- automatic hypothesis decisions;
- evidence weighting or scoring;
- confidence or certainty;
- assessments;
- claims or interpretations;
- persistence schema changes;
- Event Bus or Outbox behavior;
- CLI or HTTP APIs;
- AI integrations.

## Architectural Notes

The story continues the aggregate-integrity work started in CORE-078.

The `Investigation` aggregate owns the lifecycle boundary for mutations to its
contained hypotheses, while `Hypothesis` retains responsibility for its own
entity-level transition rules and event emission.
