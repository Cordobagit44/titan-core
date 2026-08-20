# CORE-056 — Migrate SQLite Domain Event Schema

## Status

Done

## Context

SQLite domain event persistence evolved in CORE-054 to include the
`evidence_id` column required by `EvidenceAdded`.

Databases created before that change may still contain the previous
`domain_events` schema without the `evidence_id` column.

Opening one of those databases with the current repository causes reads to
fail because `SqliteDomainEventRepository.list_all()` expects the new column
to exist.

The repository must therefore bring legacy domain event schemas forward
without requiring the caller to recreate the database.

## Goal

Allow `SqliteDomainEventRepository` to open an existing legacy
`domain_events` database and migrate its schema to the current representation.

## Acceptance Criteria

- A legacy `domain_events` table without `evidence_id` can be opened by
  `SqliteDomainEventRepository`.
- Repository initialization adds the missing `evidence_id` column.
- Existing persisted domain events remain readable after migration.
- Existing event data is preserved.
- The migrated repository continues to support the current domain event
  representation.
- Migration happens automatically when the repository is initialized.
- Existing SQLite domain event persistence behavior remains unchanged.
- The complete test suite remains green.
- Ruff passes.
- mypy passes.

## Implementation Notes

`SqliteDomainEventRepository` inspects the existing `domain_events` schema
during initialization.

When the legacy schema does not contain `evidence_id`, the repository upgrades
the table by adding the missing column.

The migration is additive and preserves existing rows.

This keeps schema evolution inside the SQLite infrastructure implementation
and does not introduce migration concerns into the domain or application
layers.

## Test Coverage

Infrastructure coverage creates a SQLite database using the legacy
`domain_events` schema, inserts an existing domain event, and then initializes
`SqliteDomainEventRepository` against that database.

The test verifies that the repository can read the previously persisted event
after initialization, demonstrating that the legacy schema was migrated
successfully.

## Architectural Notes

- Migration logic remains in the infrastructure layer.
- Domain event definitions remain unchanged.
- Application use cases remain unchanged.
- `DomainEventRepository` remains unchanged.
- Existing persisted events are preserved.
- No external migration framework introduced.
- No Unit of Work introduced.
- No Event Bus introduced.
- No Outbox introduced.
- No transaction coordination introduced.

## Validation

- pytest — 110 passed
- Ruff — passed
- mypy — 27 source files checked
