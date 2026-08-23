# CORE-077 — Refresh Project Context

## Status

Done

## Context

`docs/PROJECT_CONTEXT.md` is the continuity document used to recover TITAN Core
state across development sessions and conversations.

The document still described the repository as if CORE-042 were the latest
completed story. It also described evidence provenance, source information, and
supporting or weakening relationships as future capabilities even though those
capabilities were implemented in CORE-073 through CORE-075 and documented in
CORE-076.

This stale continuity state created a concrete risk: a future development
session could reconstruct an obsolete architecture and repeat completed work.

## Goal

Bring `docs/PROJECT_CONTEXT.md` into alignment with the current implementation
through CORE-076 so that it remains a trustworthy recovery point for future
sessions.

## Documentation Changes

The refreshed context now reflects:

- evidence description, source, and relationship classification;
- `EvidenceRelationship.SUPPORTS`, `WEAKENS`, and legacy `UNSPECIFIED`;
- the current domain event set, including hypothesis status and evidence-added
  events;
- Unit of Work transaction coordination;
- application composition through `bootstrap()` and `TitanApplication`;
- explicit application lifecycle cleanup;
- current SQLite persistence and legacy evidence schema migration behavior;
- the development state through CORE-076;
- the 147-test validation state, Ruff passing, and mypy passing on 60 source
  files;
- the GitHub pull-request and CI workflow now used for development;
- continuity instructions that direct future sessions to inspect the live
  repository before selecting the next story.

## Acceptance Criteria

- `PROJECT_CONTEXT.md` no longer identifies CORE-042 as the current state.
- Implemented evidence provenance and relationship behavior is described as
  current functionality, not future functionality.
- Current application, transaction, event persistence, and composition
  boundaries are accurately described.
- The document identifies CORE-076 as the latest completed story at the start of
  CORE-077.
- The next development step does not predefine an unaccepted implementation
  capability.
- No production code changes.
- No runtime dependency changes.
- Existing quality gates remain green.

## Out of Scope

CORE-077 does not introduce:

- new domain behavior;
- new application behavior;
- new persistence behavior;
- new evidence relationship types;
- evidence weighting or scoring;
- confidence or certainty;
- assessments;
- claims or interpretations;
- Event Bus or Outbox;
- CLI or HTTP APIs;
- AI integrations.

## Architectural Notes

This story is documentation-only, but it addresses a development-safety issue.
The continuity document must distinguish implemented behavior from long-term
vision so that repository recovery remains reliable and completed capabilities
are not accidentally recreated.

The previous project context remains recoverable through Git history; the
refreshed document prioritizes current architectural truth and concise recovery
instructions.

## Validation

- GitHub Actions CI passed.
- Ruff lint passed.
- Ruff format check passed.
- mypy passed.
- pytest passed with 147 tests.
- No production files changed.
