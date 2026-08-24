# CORE-090 — Migrate Minimal Domain Event Schema

## Status

Done

## Context

The SQLite domain-event migration rebuilds older tables into the current event
schema. It currently assumes that optional columns such as `closed_at`,
`hypothesis_statement`, and `hypothesis_id` already exist in the source table.
An earlier table containing only the original investigation-created fields
therefore triggers migration but fails while copying rows.

## Goal

Allow the event repository to migrate a minimal historical event table by
mapping absent optional columns to `NULL` while preserving existing events.

## Acceptance Criteria

- Migration detects every missing current event column.
- Missing optional source columns are copied as `NULL`.
- Existing event identifiers and payload fields are preserved.
- The migrated table accepts current hypothesis and evidence events.
- Current schemas remain unchanged.
- No public API, domain rule, event type, or dependency changes.
- The complete test suite and quality gates pass.

## Out of Scope

- Inferring payload values absent from historical rows.
- Changing event names or event ordering.
- Introducing a general migration framework.
- Recovering malformed UUIDs or unknown event types.

## Architectural Notes

The repository continues to rebuild the table transactionally. Each optional
target column selects its source value when present and `NULL` otherwise.

## Validation

- Targeted SQLite domain-event repository tests — 12 passed
- pytest — 177 passed
- Ruff lint — passed
- Ruff format — 170 files already formatted
- mypy — 65 source files checked
