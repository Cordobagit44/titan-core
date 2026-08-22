# CORE-071 — Update Project README

## Status

Done

## Context

The project README still described TITAN Core as the initial CORE-000 bootstrap
with no implemented business behavior.

The repository has since evolved to include a complete investigation domain,
application use cases, SQLite persistence, domain event persistence, Unit of
Work transaction coordination, an application composition root, architecture
guards, and end-to-end acceptance coverage.

The README no longer represented the actual state of the project.

## Goal

Update the project README so that it accurately describes the current TITAN
Core capabilities, architecture, application API, development workflow, and
scope.

## Acceptance Criteria

- Remove the obsolete CORE-000 project status.
- Describe the currently implemented investigation capabilities.
- Document the domain, application, infrastructure, and composition boundaries.
- Document SQLite persistence and Unit of Work transaction coordination.
- Document `bootstrap(database)` and `TitanApplication`.
- Document all application use cases currently exposed by the composition root.
- Provide a minimal persisted investigation workflow example.
- Document the testing strategy and architecture guards.
- Document the current development and validation commands.
- Clearly state functionality that is outside the current scope.
- Do not change production behavior.
- Do not introduce new runtime dependencies.

## Architectural Notes

The README describes the dependency direction and responsibilities of the
current architecture without introducing new architectural concepts.

The documented application API was verified against `src/titan/bootstrap.py`.

The README continues to present TITAN Core as independent from user interfaces,
web frameworks, and AI providers.

No production code is changed in this story.

## Validation

- README application API verified against `TitanApplication`.
- README saved without a UTF-8 BOM.
- pytest — 136 passed
- Ruff — passed
- mypy — 60 source files checked

## Out of Scope

Repository-wide Ruff formatting cleanup is not part of this story.

A separate formatting cleanup may address files currently reported by
`ruff format --check .`.
