# CORE-134 — Refresh README for Thesis Workflow

## Context

The README predates the completed thesis vertical slice. It reports 256 tests,
omits `Thesis` from the domain and persistence descriptions, and does not show
or list the transactional `add_thesis` use case.

## Goal

Align the public project README with the validated state after CORE-133.

## Acceptance Criteria

- Status capabilities include investigation-owned, SQLite-persisted theses.
- The documented test count is 292.
- Domain and infrastructure descriptions include thesis support.
- Application usage demonstrates thesis creation before closure.
- The exposed use-case list includes `add_thesis`.
- Reconstructed state explicitly includes claims, interpretations, and theses.
- No production code, API, schema, test, or dependency changes.
- The complete quality gates pass.

## Out of Scope

- New thesis semantics or behavior.
- Assessment, selection, invalidation, synthesis, HTTP, CLI, or AI integration.

## Architectural Notes

README examples remain concise and use only the public composed application
surface already verified by acceptance coverage.
