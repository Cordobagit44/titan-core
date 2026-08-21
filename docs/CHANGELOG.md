# TITAN Core – Changelog

This document summarizes the functional evolution of TITAN Core.

It complements the Git history and the functional specifications by providing a concise overview of completed stories.

## CORE-059 — Migrate Create Investigation to Unit of Work

### Changed

- `CreateInvestigation` now receives a `UnitOfWork`
- Investigation persistence uses `unit_of_work.investigations`
- Domain event persistence uses `unit_of_work.domain_events`
- Successful persistence commits the Unit of Work
- Persistence failures roll back the Unit of Work

### Architectural Notes

- `CreateInvestigation` now defines an explicit transaction boundary
- Repository implementations remain behind the `UnitOfWork` abstraction
- `persist_domain_events()` remains the shared event persistence mechanism
- No other application use case migrated
- No Event Bus introduced
- No Outbox introduced

### Validation

- pytest — 116 passed
- Ruff — passed
- mypy — 56 source files checked

---

## CORE-058 — Implement SQLite Unit of Work

### Added

- SQLite `SqliteUnitOfWork` implementation
- Shared SQLite connection for investigation and domain event repositories
- Explicit transaction commit coordination
- Explicit transaction rollback coordination
- Integration tests covering commit and rollback behavior

### Changed

- `SqliteInvestigationRepository` can use an externally managed SQLite connection
- `SqliteDomainEventRepository` can use an externally managed SQLite connection
- Repositories managed by `SqliteUnitOfWork` defer transaction control to the Unit of Work
- Standalone SQLite repositories preserve their existing transaction behavior

### Architectural Notes

- Transaction coordination remains in the SQLite infrastructure layer
- The application-level `UnitOfWork` abstraction remains unchanged
- Investigation and domain event repositories share one connection when managed by `SqliteUnitOfWork`
- Existing application use cases remain unchanged
- No Event Bus introduced
- No Outbox introduced
- No nested transactions introduced
- No distributed transactions introduced

### Validation

- pytest — 114 passed
- Ruff — passed
- mypy — 57 source files checked

---

## CORE-057 — Introduce Unit of Work

### Added

- Application-level `UnitOfWork` abstraction
- Access to an `InvestigationRepository` through the Unit of Work
- Access to a `DomainEventRepository` through the Unit of Work
- Explicit `commit()` operation
- Explicit `rollback()` operation
- Tests verifying that `UnitOfWork` is abstract
- Tests verifying the required Unit of Work contract

### Architectural Notes

- `UnitOfWork` belongs to the application layer
- The abstraction contains no SQLite-specific behavior
- Existing repository abstractions remain unchanged
- Existing application use cases remain unchanged
- Existing persistence behavior remains unchanged
- No SQLite Unit of Work implementation introduced
- No shared SQLite connection introduced
- No transaction coordination introduced yet
- No Event Bus introduced
- No Outbox introduced

### Validation

- pytest — 112 passed
- Ruff — passed
- mypy — 28 source files checked

---

## CORE-056 — Migrate SQLite Domain Event Schema

### Added

- Automatic migration support for legacy SQLite `domain_events` schemas
- Detection of legacy schemas without `evidence_id`
- Detection of legacy schemas where `investigation_id` is still `NOT NULL`
- Preservation of existing domain event rows during migration
- Infrastructure test covering migration from a legacy domain event schema
- Verification that migrated databases can persist current `EvidenceAdded` events

### Changed

- `SqliteDomainEventRepository` now initializes the current schema through a dedicated schema initialization path
- Legacy `domain_events` tables are rebuilt using the current representation when migration is required
- Existing event identifiers and event ordering are preserved during migration
- `investigation_id` becomes nullable in migrated schemas
- `evidence_id` is added to migrated schemas

### Architectural Notes

- Schema migration remains inside the SQLite infrastructure layer
- Domain event definitions remain unchanged
- Application use cases remain unchanged
- `DomainEventRepository` remains unchanged
- Existing persisted event data is preserved
- No external migration framework introduced
- No Unit of Work introduced
- No Event Bus introduced
- No Outbox introduced
- No transaction coordination introduced

### Validation

- pytest — 110 passed
- Ruff — passed
- mypy — 27 source files checked

---

## CORE-055 — Persist Evidence Added Domain Event

### Added

- `AddEvidence` now receives a `DomainEventRepository`
- Persistence of the `EvidenceAdded` event produced when adding evidence to a hypothesis
- Tests verifying that adding evidence still returns the created evidence
- Tests verifying that the evidence remains attached to the selected hypothesis
- Tests verifying that the generated `EvidenceAdded` event is persisted
- Verification that the persisted event preserves the original `HypothesisId`
- Verification that the persisted event preserves the original `EvidenceId`
- Existing lookup behavior for missing investigations and hypotheses remains unchanged
- Existing evidence description validation remains unchanged

### Changed

- `AddEvidence` now delegates pending domain event persistence to the shared `persist_domain_events()` application mechanism
- Pending domain events are persisted from the `Hypothesis` entity
- Investigation persistence still occurs before pending hypothesis domain events are persisted

### Architectural Notes

- Reuses the shared application-level event persistence mechanism introduced in CORE-045
- Reuses `EvidenceAdded` introduced in CORE-053
- Reuses SQLite support for `EvidenceAdded` introduced in CORE-054
- `AddEvidence` does not implement its own event-persistence loop
- Domain behavior remains independent from persistence infrastructure
- No Unit of Work introduced
- No Event Bus introduced
- No Outbox introduced
- No transaction coordination introduced

### Validation

- pytest ✅ — 109 passed
- Ruff ✅
- mypy ✅ — 27 source files checked

---
---

## CORE-054 — Add SQLite Support for Evidence Added Event

### Added

- SQLite persistence support for `EvidenceAdded`
- Restoration of `EvidenceAdded` events through `list_all()`
- Preservation of the original `HypothesisId`
- Preservation of the original `EvidenceId`
- `evidence_id` storage in the SQLite domain event representation
- Infrastructure test covering persistence and restoration of `EvidenceAdded`

### Changed

- `SqliteDomainEventRepository` now accepts `EvidenceAdded`
- `SqliteDomainEventRepository` now serializes and restores `EvidenceId`
- `hypothesis_id` serialization now also supports `EvidenceAdded`
- The SQLite `domain_events` representation now includes an `evidence_id` column

### Architectural Notes

- `EvidenceAdded` is persisted without inventing an `InvestigationId`
- The `EvidenceAdded` domain event definition remains unchanged
- Existing investigation event persistence remains unchanged
- Existing hypothesis event persistence remains unchanged
- `AddEvidence` was not modified
- No Unit of Work introduced
- No Event Bus introduced
- No Outbox introduced
- No transaction coordination introduced
- Database migration support remains outside the scope of this story
- Application-level persistence of `EvidenceAdded` remains available for a subsequent story

### Validation

- pytest ✅ — 108 passed
- Ruff ✅
- mypy ✅ — 27 source files checked

---

## CORE-053 — Emit Evidence Added Domain Event

### Added

- `EvidenceAdded` domain event
- `EvidenceAdded` preserves the `HypothesisId` of the hypothesis receiving the evidence
- `EvidenceAdded` preserves the `EvidenceId` of the evidence that was added
- `Hypothesis.add_evidence()` now records an `EvidenceAdded` event
- Domain test verifying that adding evidence emits exactly one `EvidenceAdded` event
- Domain test verifying that the emitted event preserves the original `HypothesisId`
- Domain test verifying that the emitted event preserves the original `EvidenceId`

### Changed

- `HypothesisEvent` now includes `EvidenceAdded`
- Evidence collection mutation and event recording remain coordinated by `Hypothesis`

### Architectural Notes

- `Hypothesis` records `EvidenceAdded` because it owns the evidence collection mutation
- `Evidence` remains an immutable domain object and does not become an `Entity`
- `EvidenceAdded` does not introduce persistence concerns into the domain layer
- No application use case was modified
- No repository was modified
- No SQLite persistence was introduced for `EvidenceAdded`
- No Unit of Work introduced
- No Event Bus introduced
- No Outbox introduced
- No transaction coordination introduced
- Durable persistence of `EvidenceAdded` remains available for a subsequent story

### Validation

- pytest ✅ — 107 passed
- Ruff ✅
- mypy ✅ — 27 source files checked

---

## CORE-052 — Persist Rejected Hypothesis Domain Event

### Added

- `RejectHypothesis` now receives a `DomainEventRepository`
- Persistence of the `HypothesisRejected` event produced when rejecting a hypothesis
- Tests verifying that rejecting a hypothesis still returns the rejected hypothesis
- Tests verifying that the hypothesis status is still changed to `REJECTED`
- Tests verifying that the generated `HypothesisRejected` event is persisted
- Verification that the persisted event preserves the original `HypothesisId`
- Existing lookup behavior for missing investigations and hypotheses remains unchanged

### Changed

- `RejectHypothesis` now delegates pending domain event persistence to the shared `persist_domain_events()` application mechanism
- Pending domain events are persisted from the `Hypothesis` entity
- Investigation persistence still occurs before pending hypothesis domain events are persisted

### Architectural Notes

- Reuses the shared application-level event persistence mechanism introduced in CORE-045
- Reuses SQLite support for hypothesis status events introduced in CORE-050
- `RejectHypothesis` does not implement its own event-persistence loop
- Domain behavior remains independent from persistence infrastructure
- No Unit of Work introduced
- No Event Bus introduced
- No Outbox introduced
- No transaction coordination introduced

### Validation

- pytest ✅ — 106 passed
- Ruff ✅
- mypy ✅ — 27 source files checked

---

## CORE-051 — Persist Confirmed Hypothesis Domain Event

### Added

- `ConfirmHypothesis` now receives a `DomainEventRepository`
- Persistence of the `HypothesisConfirmed` event produced when confirming a hypothesis
- Tests verifying that confirming a hypothesis still returns the confirmed hypothesis
- Tests verifying that the hypothesis status is still changed to `CONFIRMED`
- Tests verifying that the generated `HypothesisConfirmed` event is persisted
- Verification that the persisted event preserves the original `HypothesisId`
- Existing lookup behavior for missing investigations and hypotheses remains unchanged

### Changed

- `ConfirmHypothesis` now delegates pending domain event persistence to the shared `persist_domain_events()` application mechanism
- Pending domain events are persisted from the `Hypothesis` entity
- Investigation persistence still occurs before pending hypothesis domain events are persisted

### Architectural Notes

- Reuses the shared application-level event persistence mechanism introduced in CORE-045
- Reuses SQLite support for hypothesis status events introduced in CORE-050
- `ConfirmHypothesis` does not implement its own event-persistence loop
- Domain behavior remains independent from persistence infrastructure
- No Unit of Work introduced
- No Event Bus introduced
- No Outbox introduced
- No transaction coordination introduced

### Validation

- pytest ✅ — 105 passed
- Ruff ✅
- mypy ✅ — 27 source files checked

---

## CORE-050 — Add SQLite Support for Hypothesis Status Events

### Added

- SQLite persistence support for `HypothesisConfirmed`
- SQLite persistence support for `HypothesisRejected`
- Restoration of `HypothesisConfirmed` events through `list_all()`
- Restoration of `HypothesisRejected` events through `list_all()`
- Preservation of the original `HypothesisId` for both hypothesis status event types
- Tests covering persistence and restoration of both hypothesis status events

### Changed

- The SQLite `domain_events.investigation_id` column now allows `NULL`
- `SqliteDomainEventRepository` now supports domain events that contain a `HypothesisId` without an `InvestigationId`
- `hypothesis_id` serialization now supports `HypothesisRemoved`, `HypothesisConfirmed`, and `HypothesisRejected`

### Architectural Notes

- Hypothesis status events are persisted without inventing an `InvestigationId`
- Domain event definitions remain unchanged
- Existing investigation event persistence remains unchanged
- Existing `HypothesisAdded` and `HypothesisRemoved` persistence remains unchanged
- No application use cases were modified
- No Unit of Work introduced
- No Event Bus introduced
- No Outbox introduced
- No transaction coordination introduced
- Database migration support remains outside the scope of this story

### Validation

- pytest ✅ — 104 passed
- Ruff ✅
- mypy ✅ — 27 source files checked

---

## CORE-049 — Persist Hypothesis Removed Domain Event

### Added

- `RemoveHypothesis` now receives a `DomainEventRepository`
- Persistence of the `HypothesisRemoved` event produced when removing a hypothesis
- Tests verifying that removing a hypothesis still removes it from the investigation
- Tests verifying that the generated `HypothesisRemoved` event is persisted
- Verification that the persisted event preserves the removed `HypothesisId`
- Existing lookup behavior for missing investigations and hypotheses remains unchanged

### Changed

- `RemoveHypothesis` now delegates pending domain event persistence to the shared `persist_domain_events()` application mechanism
- Investigation persistence still occurs before pending domain events are persisted

### Architectural Notes

- Reuses the shared application-level event persistence mechanism introduced in CORE-045
- `RemoveHypothesis` does not implement its own event-persistence loop
- Domain behavior remains independent from persistence infrastructure
- No Unit of Work introduced
- No Event Bus introduced
- No Outbox introduced
- No transaction coordination introduced

### Validation

- pytest ✅ — 102 passed
- Ruff ✅
- mypy ✅ — 27 source files checked

---

## CORE-048 — Persist Hypothesis Added Domain Event

### Added

- `AddHypothesis` now receives a `DomainEventRepository`
- Persistence of the `HypothesisAdded` event produced when adding a hypothesis
- Tests verifying that adding a hypothesis still returns the created hypothesis
- Tests verifying that the created hypothesis remains attached to the investigation
- Tests verifying that the generated `HypothesisAdded` event is persisted
- Verification that the persisted event preserves the hypothesis statement

### Changed

- `AddHypothesis` now delegates pending domain event persistence to the shared `persist_domain_events()` application mechanism
- Investigation persistence still occurs before pending domain events are persisted

### Architectural Notes

- Reuses the shared application-level event persistence mechanism introduced in CORE-045
- `AddHypothesis` does not implement its own event-persistence loop
- Domain behavior remains independent from persistence infrastructure
- No Unit of Work introduced
- No Event Bus introduced
- No Outbox introduced
- No transaction coordination introduced

### Validation

- pytest ✅ — 101 passed
- Ruff ✅
- mypy ✅ — 27 source files checked

---

## CORE-047 — Persist Reopened Investigation Domain Event

### Added

- `ReopenInvestigation` now receives a `DomainEventRepository`
- Persistence of the `InvestigationReopened` event produced during investigation reopening
- Tests verifying that reopening still returns the investigation in `ACTIVE` status
- Tests verifying that reopening still clears `closed_at`
- Tests verifying that the generated `InvestigationReopened` event is persisted

### Changed

- `ReopenInvestigation` now delegates pending domain event persistence to the shared `persist_domain_events()` application mechanism
- Investigation persistence still occurs before pending domain events are persisted

### Architectural Notes

- Reuses the shared application-level event persistence mechanism introduced in CORE-045
- `ReopenInvestigation` does not implement its own event-persistence loop
- Domain behavior remains independent from persistence infrastructure
- No Unit of Work introduced
- No Event Bus introduced
- No Outbox introduced
- No transaction coordination introduced

### Validation

- pytest ✅ — 100 passed
- Ruff ✅
- mypy ✅ — 27 source files checked

---

## CORE-046 — Persist Closed Investigation Domain Event

### Added

- `CloseInvestigation` now receives a `DomainEventRepository`
- Persistence of the `InvestigationClosed` event produced during investigation closing
- Tests verifying that closing still changes and returns the investigation
- Tests verifying that the generated `InvestigationClosed` event is persisted
- Verification that the persisted event preserves the investigation's `closed_at` timestamp

### Changed

- `CloseInvestigation` now delegates pending domain event persistence to the shared `persist_domain_events()` application mechanism
- Investigation persistence still occurs before pending domain events are persisted

### Architectural Notes

- Reuses the shared application-level event persistence mechanism introduced in CORE-045
- `CloseInvestigation` does not implement its own event-persistence loop
- Domain behavior remains independent from persistence infrastructure
- No Unit of Work introduced
- No Event Bus introduced
- No Outbox introduced
- No transaction coordination introduced

### Validation

- pytest ✅ — 99 passed
- Ruff ✅
- mypy ✅ — 27 source files checked

---

## CORE-045 — Centralize Domain Event Persistence

### Added

- Shared application-level `persist_domain_events()` mechanism
- Generic support for persisting pending events from `Entity[EventT]`
- Tests verifying that all pending domain events are persisted
- Tests verifying that persisted events are removed from the entity's pending event collection

### Changed

- `CreateInvestigation` now delegates pending domain event persistence to `persist_domain_events()`
- `ActivateInvestigation` now delegates pending domain event persistence to `persist_domain_events()`
- Duplicated domain event persistence loops were removed from both application use cases

### Architectural Notes

- Domain event persistence coordination remains in the application layer
- `Entity` remains independent from persistence infrastructure
- `DomainEventRepository` remains unchanged
- No Unit of Work introduced
- No Event Bus introduced
- No Outbox introduced
- No transaction coordination introduced
- The shared mechanism was introduced only after repeated event-persistence coordination appeared in CORE-043 and CORE-044

### Validation

- pytest ✅ — 98 passed
- Ruff ✅
- mypy ✅ — 27 source files checked

---

## CORE-044 — Persist Activated Investigation Domain Event

### Added

- `ActivateInvestigation` now receives a `DomainEventRepository`
- Persistence of the `InvestigationActivated` event produced during investigation activation
- Coordination between investigation persistence and domain event persistence at the application use-case level
- Existing lookup validation for missing investigations remains unchanged
- Tests verifying that activation still changes and persists the investigation
- Tests verifying that the generated `InvestigationActivated` event is persisted

### Architectural Notes

- No Unit of Work introduced
- No Event Bus introduced
- No Outbox introduced
- No generalized event dispatch abstraction introduced
- `CreateInvestigation` was not refactored as part of this story
- CORE-043 and CORE-044 provide two concrete examples of explicit domain event persistence from application use cases

### Validation

- pytest ✅ — 96 passed
- Ruff ✅
- mypy ✅ — 26 source files checked

---

## CORE-043 — Persist Created Investigation Domain Event

### Added

- `CreateInvestigation` now receives a `DomainEventRepository`
- Persistence of the `InvestigationCreated` event produced during investigation creation
- Coordination between investigation persistence and domain event persistence at the application use-case level
- Tests verifying that investigation creation still saves and returns the investigation
- Tests verifying that the generated `InvestigationCreated` event is persisted

### Architectural Notes

- No Unit of Work introduced
- No Event Bus introduced
- No Outbox introduced
- No generalized event dispatch abstraction introduced
- Event persistence remains explicit and limited to `CreateInvestigation` in this story

### Validation

- pytest ✅ — 96 passed
- Ruff ✅
- mypy ✅ — 26 source files checked

---

## CORE-042 — Add SQLite Domain Event Repository

### Added

- `SqliteDomainEventRepository` infrastructure implementation
- Durable SQLite persistence of investigation domain events
- Ordered retrieval of persisted domain events
- Persistence across repository reinstantiation
- Support for `InvestigationCreated`
- Support for `InvestigationActivated`
- Support for `InvestigationClosed`
- Preservation of `InvestigationClosed.closed_at`
- Support for `InvestigationReopened`
- Support for `HypothesisAdded`
- Preservation of `HypothesisAdded.hypothesis_statement`
- Support for `HypothesisRemoved`
- Preservation of `HypothesisRemoved.hypothesis_id`
- Tests covering all current investigation domain event types

### Validation

- pytest ✅ — 95 passed
- Ruff ✅
- mypy ✅

---

## CORE-041 — Persist Investigation Domain Events

### Added

- `DomainEventRepository` application-level abstraction
- `InMemoryDomainEventRepository` implementation
- In-memory persistence of investigation domain events
- Ordered retrieval of persisted domain events
- Support for persisting multiple events without overwriting previous events
- Tests for the domain event repository abstraction and in-memory implementation

### Validation

- pytest ✅ — 88 passed
- Ruff ✅
- mypy ✅

---

## CORE-040 — Emit InvestigationReopened Event

### Added

- `InvestigationReopened` domain event
- `reopen()` now publishes the `InvestigationReopened` domain event
- Domain event registration for investigation reopening
- Domain test validating the emitted event

### Validation

- pytest ✅
- Ruff ✅
- mypy ✅

---

## CORE-039 — Reopen Investigation Use Case

### Added

- `ReopenInvestigation` application use case
- Application orchestration for reopening investigations
- Persistence of reopened investigations through the repository
- Lookup validation for missing investigations

### Validation

- pytest ✅
- Ruff ✅
- mypy ✅

---

## CORE-038 — Close Investigation Use Case

### Added

- `CloseInvestigation` application use case
- Application orchestration for closing investigations
- Persistence of closed investigations through the repository
- Lookup validation for missing investigations

### Validation

- pytest ✅
- Ruff ✅
- mypy ✅

---

## CORE-037 — Record Investigation Closure

### Added

- `Investigation.closed_at`
- `InvestigationClosed` domain event
- `close()` records the closure timestamp
- `close()` publishes the `InvestigationClosed` domain event
- `reopen()` clears `closed_at`
- SQLite persistence for `closed_at`
- SQLite restoration of `closed_at`

### Validation

- pytest ✅
- Ruff ✅
- mypy ✅
