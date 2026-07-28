# TITAN Core Backlog

## Vision

Build a clean, test-driven Domain-Driven Design investment research engine.

---

## Epic 1 — Investigation Lifecycle

| ID | Story | Status |
|----|-------|--------|
| CORE-001 | Create Investigation | Done |
| CORE-002 | Validate Investigation Title | Done |
| CORE-003 | Emit InvestigationCreated Event | Done |
| CORE-004 | Introduce InvestigationId | Done |
| CORE-005 | Add InvestigationId to Event | Done |
| CORE-006 | Activate Investigation | Done |
| CORE-007 | Emit InvestigationActivated Event | Done |

---

## Epic 2 — Hypotheses and Evidence

| ID | Story | Status |
|----|-------|--------|
| CORE-008 | Create Hypothesis Entity | Done |
| CORE-009 | Add Hypothesis to Investigation | Done |
| CORE-010 | Emit HypothesisAdded Event | Done |
| CORE-011 | Prevent Duplicate Hypotheses | Done |
| CORE-012 | Introduce HypothesisId | Done |
| CORE-013 | Add Evidence to Hypothesis | Done |
| CORE-014 | Introduce Hypothesis Status | Done |
| CORE-015 | Emit Hypothesis Status Events | Done |
| CORE-016 | Extract Entity Base Class | Done |

---

## Epic 3 — Application and Persistence

| ID | Story | Status |
|----|-------|--------|
| CORE-017 | Introduce Investigation Repository | Done |
| CORE-018 | Add In-Memory Investigation Repository | Done |
| CORE-019 | Create Investigation Use Case | Done |
| CORE-020 | Add Hypothesis Use Case | Done |
| CORE-021 | Add Hypothesis Lookup | Done |
| CORE-022 | Confirm Hypothesis Use Case | Done |
| CORE-023 | Reject Hypothesis Use Case | Done |
| CORE-024 | Add Evidence Use Case | Done |
| CORE-025 | Activate Investigation Use Case | Done |
| CORE-026 | Get Investigation Use Case | Done |
| CORE-027 | List Investigations Use Case | Done |
| CORE-028 | Remove Hypothesis Use Case | Done |
| CORE-029 | Add SQLite Investigation Repository | Done |
| CORE-030 | Persist Investigation Status | Done |
| CORE-031 | Persist Investigation Hypotheses | Done |
| CORE-032 | Persist Hypothesis Evidences | Done |

---

## Epic 4 — Investigation Closing

| ID | Story | Status |
|----|-------|--------|
| CORE-033 | Close Investigation | Done |
| CORE-034 | Prevent Modifications on Closed Investigations | Done |
| CORE-035 | Persist Closed Investigation Status | Done |
| CORE-036 | Reopen Investigation | Done |
| CORE-037 | Record Investigation Closure | Done |
| CORE-038 | Add Close Investigation Use Case | Done |
| CORE-039 | Add Reopen Investigation Use Case | Done |
| CORE-040 | Emit InvestigationReopened Event | Done |
| CORE-041 | Persist Investigation Domain Events | Planned |

---

## Current Story

### CORE-041 — Persist Investigation Domain Events

Introduce infrastructure support for persisting emitted domain events so they can be published reliably by external consumers while keeping the domain model independent of infrastructure concerns.
