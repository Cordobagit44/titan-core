# CORE-074 — Update README for Evidence Provenance

## Status

Done

## Context

CORE-073 introduced required evidence sources and preserved evidence provenance
through the domain, application use case, SQLite persistence, schema migration,
and acceptance workflow.

The project README still reflected the pre-CORE-073 application API and test
count.

It also did not document the explicit application lifecycle operation
introduced in CORE-072.

## Goal

Update the public project README so it reflects the current TITAN Core
application API and validation state.

## Acceptance Criteria

- Update the documented test count from 136 to 142.
- Update the `add_evidence()` usage example to include `source`.
- Document explicit application resource cleanup through
  `application.close()`.
- State that persisted application reconstruction includes evidence provenance.
- Preserve the existing architecture description.
- Preserve the existing project scope.
- Do not change production code.
- Do not introduce new runtime dependencies.

## Documentation Changes

The README now demonstrates:

- creating an application through `bootstrap()`;
- creating and activating an investigation;
- adding a hypothesis;
- adding evidence with an explicit source;
- confirming the hypothesis;
- closing the investigation;
- retrieving persisted state;
- listing investigations;
- releasing application resources with `application.close()`.

The README also reflects the current suite size of 142 passing tests.

## Architectural Notes

- CORE-074 is documentation-only.
- Evidence provenance behavior was implemented in CORE-073.
- Application lifecycle management was implemented in CORE-072.
- No domain behavior changed.
- No application behavior changed.
- No SQLite behavior changed.
- No CLI, HTTP API, Event Bus, Outbox, or AI integration was introduced.

## Validation

- README usage matches the current `AddEvidence` signature.
- README lifecycle usage matches `TitanApplication.close()`.
- pytest — 142 passed
- Ruff — passed
- mypy — 60 source files checked
