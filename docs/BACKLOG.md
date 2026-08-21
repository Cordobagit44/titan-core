# TITAN Core Backlog

## Vision

Build a clean, test-driven Domain-Driven Design investment research engine.

---

## Epic 1 — Investigation Lifecycle

| ID       | Story                             | Status |
| -------- | --------------------------------- | ------ |
| CORE-001 | Create Investigation              | Done   |
| CORE-002 | Validate Investigation Title      | Done   |
| CORE-003 | Emit InvestigationCreated Event   | Done   |
| CORE-004 | Introduce InvestigationId         | Done   |
| CORE-005 | Add InvestigationId to Event      | Done   |
| CORE-006 | Activate Investigation            | Done   |
| CORE-007 | Emit InvestigationActivated Event | Done   |

---

## Epic 2 — Hypotheses and Evidence

| ID       | Story                           | Status |
| -------- | ------------------------------- | ------ |
| CORE-008 | Create Hypothesis Entity        | Done   |
| CORE-009 | Add Hypothesis to Investigation | Done   |
| CORE-010 | Emit HypothesisAdded Event      | Done   |
| CORE-011 | Prevent Duplicate Hypotheses    | Done   |
| CORE-012 | Introduce HypothesisId          | Done   |
| CORE-013 | Add Evidence to Hypothesis      | Done   |
| CORE-014 | Introduce Hypothesis Status     | Done   |
| CORE-015 | Emit Hypothesis Status Events   | Done   |
| CORE-016 | Extract Entity Base Class       | Done   |

---

## Epic 3 — Application and Persistence

| ID       | Story                                  | Status |
| -------- | -------------------------------------- | ------ |
| CORE-017 | Introduce Investigation Repository     | Done   |
| CORE-018 | Add In-Memory Investigation Repository | Done   |
| CORE-019 | Create Investigation Use Case          | Done   |
| CORE-020 | Add Hypothesis Use Case                | Done   |
| CORE-021 | Add Hypothesis Lookup                  | Done   |
| CORE-022 | Confirm Hypothesis Use Case            | Done   |
| CORE-023 | Reject Hypothesis Use Case             | Done   |
| CORE-024 | Add Evidence Use Case                  | Done   |
| CORE-025 | Activate Investigation Use Case        | Done   |
| CORE-026 | Get Investigation Use Case             | Done   |
| CORE-027 | List Investigations Use Case           | Done   |
| CORE-028 | Remove Hypothesis Use Case             | Done   |
| CORE-029 | Add SQLite Investigation Repository    | Done   |
| CORE-030 | Persist Investigation Status           | Done   |
| CORE-031 | Persist Investigation Hypotheses       | Done   |
| CORE-032 | Persist Hypothesis Evidences           | Done   |

---

## Epic 4 — Investigation Closing

| ID       | Story                                          | Status |
| -------- | ---------------------------------------------- | ------ |
| CORE-033 | Close Investigation                            | Done   |
| CORE-034 | Prevent Modifications on Closed Investigations | Done   |
| CORE-035 | Persist Closed Investigation Status            | Done   |
| CORE-036 | Reopen Investigation                           | Done   |
| CORE-037 | Record Investigation Closure                   | Done   |
| CORE-038 | Add Close Investigation Use Case               | Done   |
| CORE-039 | Add Reopen Investigation Use Case              | Done   |
| CORE-040 | Emit InvestigationReopened Event               | Done   |

---

## Epic 5 — Domain Event Persistence

| ID       | Story                                           | Status |
| -------- | ----------------------------------------------- | ------ |
| CORE-041 | Persist Investigation Domain Events             | Done   |
| CORE-042 | Add SQLite Domain Event Repository              | Done   |
| CORE-043 | Persist Created Investigation Domain Event      | Done   |
| CORE-044 | Persist Activated Investigation Domain Event    | Done   |
| CORE-045 | Centralize Domain Event Persistence             | Done   |
| CORE-046 | Persist Closed Investigation Domain Event       | Done   |
| CORE-047 | Persist Reopened Investigation Domain Event     | Done   |
| CORE-048 | Persist Hypothesis Added Domain Event           | Done   |
| CORE-049 | Persist Hypothesis Removed Domain Event         | Done   |
| CORE-050 | Add SQLite Support for Hypothesis Status Events | Done   |
| CORE-051 | Persist Confirmed Hypothesis Domain Event       | Done   |
| CORE-052 | Persist Rejected Hypothesis Domain Event        | Done   |
| CORE-053 | Emit Evidence Added Domain Event                | Done   |
| CORE-054 | Add SQLite Support for Evidence Added Event     | Done   |
| CORE-055 | Persist Evidence Added Domain Event             | Done   |
| CORE-056 | Migrate SQLite Domain Event Schema              | Done   |

---

## Epic 6 — Transaction Coordination

| ID       | Story                         | Status |
| -------- | ----------------------------- | ------ |
| CORE-057 | Introduce Unit of Work        | Done   |
| CORE-058 | Implement SQLite Unit of Work | Done   |
| CORE-059 | Migrate Create Investigation to Unit of Work | Done   |
| CORE-060 | Migrate Add Hypothesis to Unit of Work | Done   |
| CORE-061 | Migrate Add Evidence to Unit of Work | Done   |
| CORE-062 | Migrate Activate Investigation to Unit of Work | Done   |
| CORE-063 | Migrate Confirm Hypothesis to Unit of Work | Done   |

---

## Current Story

No CORE story is currently active.

CORE-063 — Migrate Confirm Hypothesis to Unit of Work is complete.

`ConfirmHypothesis` now uses the application-level `UnitOfWork` as its
persistence boundary.

Investigation state is loaded and saved through the investigation repository
exposed by the Unit of Work, while pending `HypothesisConfirmed` events are
persisted through the Unit of Work's domain event repository.

Successful persistence commits the Unit of Work. If persistence fails,
`ConfirmHypothesis` rolls back the Unit of Work before propagating the original
exception.

Missing investigation and hypothesis behavior remains unchanged.

No other application use case is migrated to Unit of Work in this story.
