# CORE-068 — Enforce Unit of Work for Mutating Use Cases

## Status

Done

## Context

CORE-057 introduced the application-level `UnitOfWork` abstraction.

CORE-058 introduced `SqliteUnitOfWork`.

CORE-059 through CORE-067 migrated all identified mutating application use cases
to use `UnitOfWork` instead of directly depending on investigation and domain
event repositories.

The application layer now follows a clear dependency rule:

- mutating use cases depend on `UnitOfWork`;
- read-only queries may depend directly on `InvestigationRepository`;
- repository abstractions, implementations, transaction helpers, and the Unit
  of Work itself may depend directly on repository abstractions.

Without an automated architecture guard, future changes could accidentally
reintroduce direct repository dependencies into mutating use cases.

## Goal

Add an automated architecture test that prevents application modules from
introducing direct repository dependencies unless they are explicitly allowed.

## Acceptance Criteria

- Add an architecture test for application-layer repository dependencies.
- Direct imports of `InvestigationRepository` and `DomainEventRepository` are
  prohibited by default.
- Existing intentional dependencies are represented by an explicit allowlist.
- Read-only query modules remain allowed to use `InvestigationRepository`.
- Repository abstractions and in-memory implementations remain allowed.
- `persist_domain_events()` remains allowed to use `DomainEventRepository`.
- `UnitOfWork` remains allowed to reference both repository abstractions.
- Mutating use cases remain free of direct repository dependencies.
- The architecture test fails when a prohibited direct dependency is introduced.

## Architectural Notes

- The rule is enforced using Python AST inspection.
- Production code is not modified by this story.
- The allowlist makes intentional exceptions explicit.
- New application modules are protected automatically unless explicitly added
  to the allowlist.
- No Event Bus introduced.
- No Outbox introduced.

## Validation

- Architecture guard passes on the current application layer.
- A temporary prohibited repository import was detected by the guard.
- Removing the temporary violation restored the test to green.
- pytest — 133 passed
- Ruff — passed
- mypy — 57 source files checked
