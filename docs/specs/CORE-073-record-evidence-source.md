# CORE-073 — Record Evidence Source

## Status

Done

## Context

TITAN Core can record evidence attached to hypotheses, but evidence previously
contained only an identifier and a description.

That representation did not preserve where the evidence originated.

For a traceable investigation system, evidence must retain an explicit source
so that a later assessment can be connected back to the origin of the
supporting information.

## Goal

Introduce a required source for evidence and preserve that source through the
domain, application, SQLite persistence, schema migration, and end-to-end
application workflow.

## Acceptance Criteria

- `Evidence` requires a `source`.
- Evidence exposes its source.
- Empty or whitespace-only sources are rejected.
- Existing evidence description validation remains unchanged.
- `EvidenceId` behavior remains unchanged.
- `AddEvidence` accepts a source.
- `AddEvidence` passes the source into the domain evidence object.
- Evidence source is persisted in SQLite.
- Evidence source is restored from SQLite.
- Existing SQLite databases without an evidence source column are migrated
  automatically.
- Legacy evidence rows are preserved during migration.
- Legacy evidence without recorded provenance receives the explicit marker
  `legacy source unavailable`.
- The persisted application workflow preserves evidence source across
  application reconstruction.
- Existing `EvidenceAdded` domain event structure remains unchanged.
- No external provenance service is introduced.
- No URL-specific source model is introduced.
- No new runtime dependency is introduced.

## Domain Model

`Evidence` now contains:

- `id`
- `description`
- `source`

`source` is intentionally modeled as a required textual reference.

The domain does not currently distinguish between URLs, documents, datasets,
files, people, APIs, or other possible source types.

That additional modeling can be introduced later if concrete requirements
justify it.

## Application Changes

`AddEvidence` now requires:

- `investigation_id`
- `hypothesis_id`
- `description`
- `source`

The use case creates the evidence with both its description and source while
preserving the existing Unit of Work transaction boundary.

## Persistence Changes

The SQLite `evidences` table now includes:

`source TEXT NOT NULL`

New evidence rows persist the source together with the evidence identifier,
hypothesis identifier, and description.

Evidence reconstruction restores the original source value.

## Schema Migration

`SqliteInvestigationRepository` inspects the `evidences` table during
initialization.

When an existing database does not contain the `source` column, the repository
adds it automatically.

Existing evidence rows receive:

`legacy source unavailable`

This marker explicitly communicates that provenance was not recorded in the
legacy schema instead of inventing a source.

## Domain Events

`EvidenceAdded` remains unchanged.

The event continues to identify:

- `hypothesis_id`
- `evidence_id`

Evidence provenance belongs to the persisted evidence model and is not copied
into the domain event in this story.

## Acceptance Coverage

The end-to-end investigation workflow now supplies an evidence source through
`TitanApplication`.

After the application is closed and reconstructed against the same SQLite
database, the restored evidence retains:

- its identifier;
- its description;
- its source.

## Architectural Notes

- Evidence provenance begins in the domain rather than infrastructure.
- Application use cases pass provenance explicitly.
- SQLite remains responsible for schema evolution.
- Legacy data is preserved.
- Missing legacy provenance is represented honestly and explicitly.
- No source-type hierarchy is introduced prematurely.
- No CLI, HTTP API, Event Bus, Outbox, or AI integration is introduced.

## Validation

- pytest — 142 passed
- Ruff — passed
- mypy — 60 source files checked
