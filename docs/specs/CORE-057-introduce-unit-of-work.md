# CORE-057 — Introduce Unit of Work Abstraction

## Status

Complete

## Context

Mutating application use cases currently coordinate investigation persistence
and domain event persistence explicitly.

The SQLite investigation repository and SQLite domain event repository each
own an independent database connection.

As a result, investigation state and its corresponding domain events cannot
currently participate in one application-controlled transaction.

Before introducing transactional SQLite coordination, the application layer
needs an abstraction representing a persistence boundary.

## Goal

Introduce an application-level `UnitOfWork` abstraction that exposes the
repositories required by mutating use cases and defines explicit transaction
completion operations.

## Acceptance Criteria

- Introduce an application-level `UnitOfWork` abstraction.
- A Unit of Work exposes an `InvestigationRepository`.
- A Unit of Work exposes a `DomainEventRepository`.
- A Unit of Work defines `commit()`.
- A Unit of Work defines `rollback()`.
- The abstraction contains no SQLite-specific behavior.
- Existing repositories remain unchanged.
- Existing application use cases remain unchanged.
- Existing persistence behavior remains unchanged.

## Architectural Notes

- `UnitOfWork` belongs to the application layer.
- Infrastructure implementations will satisfy the abstraction in subsequent
  stories.
- The abstraction must not import SQLite.
- No existing use case is refactored in this story.
- No transaction coordination is introduced yet.
- No Event Bus introduced.
- No Outbox introduced.

## Out of Scope

This story does not:

- implement `SqliteUnitOfWork`;
- share SQLite connections;
- make persistence atomic;
- modify mutating application use cases;
- change `persist_domain_events()`;
- introduce an Event Bus;
- introduce an Outbox.

## Definition of Done

- RED → GREEN → REFACTOR
- Unit of Work contract covered by tests
- Existing test suite remains green
- Ruff passes
- mypy passes
