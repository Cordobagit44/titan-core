# TITAN Core – Changelog

This document summarizes the functional evolution of TITAN Core.

It complements the Git history and the functional specifications by providing a concise overview of completed stories.

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
