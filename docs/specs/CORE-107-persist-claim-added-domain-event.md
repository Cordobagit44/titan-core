# CORE-107 — Persist ClaimAdded Domain Event

## Status

Done

## Context

`ClaimAdded` records the reasoning transition that attaches an atomic claim to
a hypothesis, but the SQLite domain-event repository does not recognize or
serialize that event.

## Goal

Persist and reconstruct `ClaimAdded` with complete identity context.

## Acceptance Criteria

- The event schema includes nullable `claim_id` storage.
- Existing event tables without `claim_id` migrate without losing rows.
- Saving `ClaimAdded` preserves hypothesis, claim, and evidence IDs.
- `list_all()` reconstructs the original event in order.
- Missing required ClaimAdded fields are rejected contextually.
- Malformed ClaimAdded UUID fields are rejected contextually.
- Existing event types, migrations, ordering, and diagnostics remain intact.
- No application use case or claim extraction behavior is introduced.
- The complete test suite and quality gates pass.

## Out of Scope

- Application orchestration.
- Claim removal or update events.
- Event replay or an event bus.
- Automatic extraction or AI integration.

## Architectural Notes

The event store remains an append-only serialization boundary. `claim_id` is
nullable because historical event types do not carry claim identity.

## Validation

- Targeted SQLite domain-event repository tests — 24 passed
- pytest — 228 passed
- Ruff lint — passed
- Ruff format — 191 files already formatted
- mypy — 69 source files checked
