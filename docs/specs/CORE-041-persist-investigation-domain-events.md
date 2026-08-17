# CORE-041 — Persist Investigation Domain Events

## Goal

As the system,

I want emitted investigation domain events to be persisted,

so that they can be retained reliably for future publication, auditing, and integration without coupling the domain model to infrastructure concerns.

## Business Rules

- Domain events remain created and recorded by the domain model.
- Persisting events must not introduce infrastructure dependencies into `titan.core`.
- Persisted events preserve their event type and investigation identifier.
- Events are persisted only after they have been emitted by the aggregate.
- Event persistence is handled through an abstraction outside the domain model.
- Existing investigation behavior remains unchanged.

## Acceptance Criteria

- An application-level abstraction exists for persisting investigation domain events.
- An in-memory implementation can store persisted domain events.
- Persisted events can be retrieved in the order in which they were stored.
- Multiple events can be persisted without overwriting previous events.
- The domain model has no dependency on the persistence implementation.
- Existing tests continue to pass.
- New tests verify domain-event persistence behavior.

## Architectural Constraints

- `titan.core` must remain independent of application and infrastructure layers.
- The `Investigation` aggregate must not know how or where events are persisted.
- Event persistence must reuse the existing domain events rather than introducing duplicate event models.
- No external message broker or framework is introduced in this story.

## Out of Scope

- Publishing events to external systems.
- Message brokers.
- Retry mechanisms.
- Transactional outbox processing.
- Event replay.
- Event sourcing.
