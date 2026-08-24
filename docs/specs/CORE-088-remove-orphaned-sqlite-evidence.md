# CORE-088 — Remove Orphaned SQLite Evidence

## Status

Done

## Context

The SQLite investigation repository replaces an investigation's persisted
hypotheses when saving the aggregate. Before replacement, it deletes evidence
only for hypotheses still present in the current aggregate. Evidence belonging
to a hypothesis removed since the previous save can therefore remain as an
orphaned row.

## Goal

Ensure saving an investigation removes persisted evidence belonging to every
previously stored hypothesis of that investigation before its hypotheses are
replaced.

## Acceptance Criteria

- Saving a hypothesis with evidence persists that evidence normally.
- Removing the pending hypothesis and saving again removes its evidence row.
- Evidence belonging to other investigations is not removed.
- Existing aggregate reconstruction behavior remains unchanged.
- No public API, domain rule, schema, event type, or dependency changes.
- The complete test suite and quality gates pass.

## Out of Scope

- Enabling SQLite foreign-key cascades globally.
- Changing repository transaction ownership.
- Editing or deleting evidence through a new application use case.
- Schema migrations or new tables.

## Architectural Notes

The correction belongs to `SqliteInvestigationRepository.save()`. Cleanup is
scoped by the persisted hypothesis rows associated with the investigation being
saved and occurs inside the existing transaction boundary.

## Validation

- Targeted SQLite investigation repository tests — 11 passed
- pytest — 175 passed
- Ruff lint — passed
- Ruff format — 168 files already formatted
- mypy — 65 source files checked
