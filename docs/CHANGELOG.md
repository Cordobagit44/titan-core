# TITAN Core – Changelog

This document summarizes the functional evolution of TITAN Core.

It complements the Git history and the functional specifications by providing a concise overview of completed stories.

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
- CORE-043 and CORE-044 now provide two concrete examples of explicit domain event persistence from application use cases

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
