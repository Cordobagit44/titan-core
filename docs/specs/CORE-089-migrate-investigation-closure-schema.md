# CORE-089 — Migrate Investigation Closure Schema

## Status

Done

## Context

Current SQLite investigation queries require the nullable `closed_at` column.
`CREATE TABLE IF NOT EXISTS` does not add that column when an existing database
contains an older `investigations` table, so opening and reading such a database
raises a SQLite error. Evidence columns already use explicit additive migration,
but investigation closure metadata does not.

## Goal

Migrate legacy `investigations` tables by adding a nullable `closed_at` column
before repository reads or writes occur.

## Acceptance Criteria

- Repository initialization detects whether `closed_at` exists.
- A missing `closed_at` column is added without replacing the table.
- Existing investigation rows and identifiers remain unchanged.
- A restored legacy investigation has `closed_at is None`.
- Current schemas are left unchanged.
- No public API, domain rule, event type, or dependency changes.
- The complete test suite and quality gates pass.

## Out of Scope

- Inventing closure timestamps for historical rows.
- Rebuilding the investigations table.
- Changing status or purpose data.
- Introducing a general migration framework.

## Architectural Notes

The migration follows the repository's existing additive evidence-schema
migration pattern and runs inside repository initialization before its managed
connection is committed.

## Validation

- Targeted SQLite investigation repository tests — 12 passed
- pytest — 176 passed
- Ruff lint — passed
- Ruff format — 169 files already formatted
- mypy — 65 source files checked
