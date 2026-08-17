# CORE-042 — SQLite Domain Event Repository

## Goal

As the system,

I want a SQLite implementation of `DomainEventRepository`,

so that persisted domain events survive process restarts without coupling the domain model to SQLite.

## Motivation

CORE-041 introduced the `DomainEventRepository` abstraction and an in-memory implementation.

The next step is to provide durable persistence while preserving the same application-level contract.

## Acceptance Criteria

- A `SqliteDomainEventRepository` implementation exists.
- The repository implements `DomainEventRepository`.
- Persisted events survive repository re-instantiation when using the same SQLite database.
- Events are returned in insertion order.
- Multiple events can be persisted without overwriting previous events.
- Persisted events preserve their concrete event type.
- Persisted events preserve the investigation identifier.
- Existing domain and application behavior remains unchanged.
- Existing tests continue to pass.

## Architectural Constraints

- `titan.core` must not depend on SQLite.
- SQLite-specific code belongs in `titan.infrastructure`.
- The application layer depends only on the repository abstraction.
- The repository must persist existing domain events rather than introduce duplicate event models.
- No external message broker or event bus is introduced in this story.

## Out of Scope

- Publishing events to external systems.
- Retry mechanisms.
- Transactional outbox processing.
- Event replay.
- Event sourcing.
- Schema migration tooling beyond what is required for this repository.

## Definition of Done

- RED → GREEN → REFACTOR completed.
- pytest passes.
- Ruff passes.
- mypy passes.
- CHANGELOG updated.
- BACKLOG updated.
