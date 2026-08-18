# CORE-045 — Centralize Domain Event Persistence

## User Story

As a maintainer,
I want pending domain event persistence to be centralized,
so that application use cases do not duplicate the same coordination logic.

## Acceptance Criteria

- A shared application-level mechanism persists all pending domain events from an entity.
- The mechanism receives a `DomainEventRepository`.
- The mechanism pulls pending events from the entity.
- Each pending event is persisted through `DomainEventRepository`.
- `CreateInvestigation` delegates domain event persistence to the shared mechanism.
- `ActivateInvestigation` delegates domain event persistence to the shared mechanism.
- Existing behavior of `CreateInvestigation` remains unchanged.
- Existing behavior of `ActivateInvestigation` remains unchanged.
- Existing domain behavior remains unchanged.
- Existing persistence abstractions remain unchanged.

## Technical Notes

- This story is a refactor.
- Do not introduce a Unit of Work.
- Do not introduce an Event Bus.
- Do not introduce an Outbox.
- Do not introduce transaction coordination.
- Do not move persistence concerns into the domain.
- Do not modify unrelated application use cases.
- Keep the shared mechanism as small as possible.

## Definition of Done

- RED → GREEN → REFACTOR
- Existing tests remain green
- Tests cover the shared event persistence mechanism
- Ruff passes
- MyPy passes
