# TITAN Core — Project Context

## Purpose

This document is the continuity and recovery reference for TITAN Core.

Its purpose is to preserve the architectural intent, development methodology,
current state, and direction of the project independently of any individual
development session or conversation.

When development resumes in a new environment or conversation, this document
should be reviewed together with:

- `docs/BACKLOG.md`
- `docs/CHANGELOG.md`
- the specifications under `docs/specs/`

---

## Vision

Build a clean, test-driven Domain-Driven Design investment research engine.

TITAN Core is intended to provide the domain and application foundation for
structured investment research.

The system models an investment research process as an investigation in which
hypotheses are formulated, evidence is collected, hypotheses are evaluated,
and the investigation progresses through an explicit lifecycle.

The core should remain independent from user interfaces, external publishing
mechanisms, and infrastructure-specific concerns.

---

## Core Domain

The primary aggregate is `Investigation`.

An investigation currently contains:

- `InvestigationId`
- title
- purpose
- investigation status
- hypotheses
- closure timestamp when applicable

An investigation controls its own lifecycle and protects its domain
invariants.

### Investigation lifecycle

Current statuses:

- `DRAFT`
- `ACTIVE`
- `CLOSED`

Supported lifecycle operations include:

- create
- activate
- close
- reopen

Closed investigations prevent modifications until reopened.

---

## Hypotheses

Investigations contain hypotheses.

A hypothesis has its own identity and lifecycle.

The domain currently supports:

- adding hypotheses
- preventing duplicate hypotheses
- finding hypotheses
- removing hypotheses
- confirming hypotheses
- rejecting hypotheses

Hypotheses may contain evidence used during the research process.

---

## Evidence

Evidence belongs to hypotheses.

Evidence has its own identity and description and is persisted together with
the investigation aggregate.

---

## Domain Events

TITAN uses domain events to represent meaningful facts that occurred inside
the domain.

Current investigation domain events include:

- `InvestigationCreated`
- `InvestigationActivated`
- `InvestigationClosed`
- `InvestigationReopened`
- `HypothesisAdded`
- `HypothesisRemoved`

Domain entities record events internally and expose them through
`pull_events()`.

The domain model does not depend on event persistence infrastructure.

---

## Application Layer

The application layer orchestrates domain behavior through use cases and
repository abstractions.

Implemented use cases include operations for:

- creating investigations
- activating investigations
- closing investigations
- reopening investigations
- retrieving investigations
- listing investigations
- adding hypotheses
- removing hypotheses
- confirming hypotheses
- rejecting hypotheses
- adding evidence

Application code depends on abstractions rather than concrete persistence
implementations.

---

## Persistence

### Investigation persistence

`InvestigationRepository` defines the application-level persistence
abstraction.

Implementations currently include:

- `InMemoryInvestigationRepository`
- `SqliteInvestigationRepository`

SQLite persistence restores:

- investigation identity
- title
- purpose
- status
- closure timestamp
- hypotheses
- hypothesis status
- evidence

### Domain event persistence

`DomainEventRepository` defines the abstraction for storing domain events.

Implementations currently include:

- `InMemoryDomainEventRepository`
- `SqliteDomainEventRepository`

The SQLite implementation provides durable, ordered domain event persistence.

It currently supports persistence and restoration of:

- `InvestigationCreated`
- `InvestigationActivated`
- `InvestigationClosed`
- `InvestigationReopened`
- `HypothesisAdded`
- `HypothesisRemoved`

Event-specific data such as closure timestamps, hypothesis statements, and
hypothesis identifiers is preserved.

---

## Architecture Principles

TITAN Core follows these principles:

### Domain-Driven Design

Business rules belong in the domain model.

Infrastructure must not leak into the domain.

### Dependency Direction

Dependencies should point inward.

The core domain must remain independent from SQLite and other infrastructure
technologies.

### Repository Abstractions

Application code works against repository abstractions.

Concrete persistence belongs in infrastructure.

### Test-Driven Development

New behavior is normally developed using:

1. RED — introduce a failing test describing the required behavior.
2. GREEN — implement the minimum behavior necessary to satisfy the test.
3. REFACTOR — improve the implementation while keeping the suite green.

Existing behavior must remain protected by the full test suite.

### Small Stories

Development proceeds through numbered CORE stories.

Each story should have a focused responsibility and should not silently expand
into unrelated architectural work.

### Quality Gates

Before a CORE story is considered complete, run:

`uv run pytest`

`uv run ruff check .`

`uv run mypy src`

All three must pass.

---

## Git Workflow

Development normally follows this workflow:

1. Start from an up-to-date `main`.
2. Create `feature/CORE-XXX`.
3. Develop using TDD.
4. Run the complete quality gates.
5. Update the specification, backlog, and changelog as appropriate.
6. Review `git status`.
7. Commit only the files belonging to the story.
8. Push the feature branch.
9. Switch to `main`.
10. Integrate using `git merge --ff-only feature/CORE-XXX`.
11. Push `main`.

Avoid unrelated changes in story commits.

---

## Source of Truth

When determining project state, prefer the repository over assumptions from a
previous development conversation.

Use:

1. Current source code and tests
2. `docs/PROJECT_CONTEXT.md`
3. `docs/BACKLOG.md`
4. `docs/CHANGELOG.md`
5. Story specifications under `docs/specs/`
6. Git history

If documentation and implementation disagree, inspect the implementation and
tests before proceeding.

---

## Current Development State

Last completed story:

`CORE-042 — Add SQLite Domain Event Repository`

Last integrated commit:

`3d0cf9e — CORE-042: add SQLite domain event repository`

Current branch after integration:

`main`

Validation at completion of CORE-042:

- pytest: 95 passed
- Ruff: passed
- mypy: passed on 26 source files

CORE-042 is integrated into `main` and pushed to `origin/main`.

---

## Next Development Step

`CORE-043` has not yet been defined.

Do not assume its requirements solely from its number.

Before implementation:

1. Review the current architecture.
2. Review `BACKLOG.md` and recent specifications.
3. Identify the next smallest architectural capability required by TITAN.
4. Define CORE-043 explicitly.
5. Write its specification.
6. Begin implementation using TDD.

A possible future direction is reliable publication or dispatch of persisted
domain events to external consumers, but this is not yet an accepted
CORE-043 requirement.

---

## Continuity Instructions

When resuming TITAN Core development in a new conversation or development
session, begin by establishing the current repository state.

Review this document, the backlog, changelog, latest specifications, and
relevant source/tests.

Do not recreate completed functionality.

Do not assume that an idea discussed previously became an accepted
requirement unless it is represented in the repository or explicitly
confirmed.

Continue from the last completed CORE story using the same incremental,
test-driven development process.
