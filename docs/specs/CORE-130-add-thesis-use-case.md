# CORE-130 — Add Thesis Use Case

## Context

The domain, SQLite aggregate repository, and event store now support theses, but
no application operation coordinates thesis creation and persistence atomically.

## Goal

Introduce transactional thesis creation and expose it through the composition root.

## Acceptance Criteria

- The use case accepts an investigation ID and thesis statement.
- It returns a newly identified `Thesis`.
- Mutation routes through `Investigation.add_thesis()`.
- Successful execution saves aggregate state and persists `ThesisAdded`.
- Successful execution commits through the Unit of Work boundary.
- Missing investigation, closed investigation, invalid statement, and event
  persistence failure roll back.
- `bootstrap()` exposes `add_thesis`.
- Existing use cases and transaction behavior remain intact.
- The complete quality gates pass.

## Out of Scope

- Thesis selection, replacement, removal, status, grounding, or assessment.
- Acceptance workflow coverage.
- HTTP, CLI, automatic synthesis, or AI integration.

## Architectural Notes

The application creates the thesis, the aggregate enforces lifecycle and
identity rules, and Unit of Work coordinates aggregate and event persistence.
