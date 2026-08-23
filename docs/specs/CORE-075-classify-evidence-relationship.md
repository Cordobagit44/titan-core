# CORE-075 — Classify Evidence Relationship

## Status

Done

## Context

TITAN Core currently records evidence with an explicit description and source.

Evidence is attached to a hypothesis, but the domain does not currently express
how that evidence relates to the hypothesis. As a result, the model can record
that evidence belongs to a hypothesis without distinguishing whether the
evidence supports or weakens it.

TITAN's longer-term reasoning model requires richer evidence relationships
before introducing higher-level concepts such as claims, assessments, scores,
or confidence.

## Goal

Allow evidence attached to a hypothesis to explicitly classify its relationship
to that hypothesis.

New evidence must state whether it supports or weakens the hypothesis.

## Domain Model

Introduce an `EvidenceRelationship` enum with these values:

- `SUPPORTS`
- `WEAKENS`
- `UNSPECIFIED`

`Evidence` records:

- description;
- source;
- relationship;
- evidence identifier.

New evidence created through the application layer must use either `SUPPORTS`
or `WEAKENS`.

`UNSPECIFIED` exists only to represent persisted legacy evidence for which no
relationship was historically recorded.

## Application Behavior

`AddEvidence` accepts an evidence relationship in addition to:

- investigation identifier;
- hypothesis identifier;
- description;
- source.

The use case creates evidence with the requested relationship and preserves the
existing Unit of Work transaction behavior.

Application callers must not create new evidence with an `UNSPECIFIED`
relationship.

## Persistence

SQLite evidence persistence stores the relationship explicitly.

Existing databases whose `evidences` table does not contain a relationship
column are migrated automatically.

Existing evidence rows are assigned the persisted legacy value corresponding
to `UNSPECIFIED`.

Saving and restoring an investigation preserves the evidence relationship.

## Domain Events

`EvidenceAdded` remains unchanged.

The event continues to identify the hypothesis and evidence. Evidence
relationship data remains part of the persisted aggregate and is not duplicated
into the event in this story.

## Acceptance Criteria

- Evidence can represent a supporting relationship.
- Evidence can represent a weakening relationship.
- Evidence relationship is preserved by SQLite persistence.
- Existing SQLite evidence schemas are migrated automatically.
- Legacy evidence can be restored with an `UNSPECIFIED` relationship.
- `AddEvidence` requires an explicit relationship for new evidence.
- `AddEvidence` rejects `UNSPECIFIED` for new evidence.
- The complete application workflow preserves evidence relationship after
  application reconstruction.
- Existing transaction behavior remains unchanged.
- Existing domain-event behavior remains unchanged.
- The complete test suite passes.
- Ruff passes.
- mypy passes.

## Out of Scope

CORE-075 does not introduce:

- evidence strength or weight;
- numeric scores;
- confidence or certainty;
- automatic hypothesis confirmation or rejection;
- assessment;
- claims or interpretations;
- thesis modeling;
- contradiction detection;
- source-type hierarchies;
- external provenance services;
- Event Bus;
- Outbox;
- CLI or HTTP APIs;
- AI integrations.

## Architectural Notes

The relationship is a domain concept because it describes the meaning of
evidence relative to a hypothesis.

The relationship does not calculate a conclusion. It records an explicit
classification supplied by the caller.

`UNSPECIFIED` is a compatibility state for historical persisted data, not a
valid classification for newly recorded evidence.

The story extends the existing evidence model incrementally without introducing
higher-level reasoning abstractions prematurely.

## Validation

- Domain relationship modeling verified
- `AddEvidence` relationship propagation verified
- `UNSPECIFIED` rejection for new evidence verified
- SQLite relationship persistence and restoration verified
- Legacy SQLite evidence schema migration verified
- Acceptance workflow preserves evidence relationship after application reconstruction
- `EvidenceAdded` behavior remains unchanged
- pytest — 147 passed
- Ruff — passed
- mypy — 60 source files checked
