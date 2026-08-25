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

| ID       | Story                                      | Status |
| -------- | ------------------------------------------ | ------ |
| CORE-057 | Introduce Unit of Work                     | Done   |
| CORE-058 | Implement SQLite Unit of Work              | Done   |
| CORE-059 | Migrate Create Investigation to Unit of Work | Done |
| CORE-060 | Migrate Add Hypothesis to Unit of Work     | Done   |
| CORE-061 | Migrate Add Evidence to Unit of Work       | Done   |
| CORE-062 | Migrate Activate Investigation to Unit of Work | Done |
| CORE-063 | Migrate Confirm Hypothesis to Unit of Work | Done   |
| CORE-064 | Migrate Reject Hypothesis to Unit of Work  | Done   |
| CORE-065 | Migrate Close Investigation to Unit of Work | Done  |
| CORE-066 | Migrate Remove Hypothesis to Unit of Work  | Done   |
| CORE-067 | Migrate Reopen Investigation to Unit of Work | Done |
| CORE-068 | Enforce Unit of Work for Mutating Use Cases | Done  |

---

## Epic 7 — Application Composition

| ID       | Story                                  | Status |
| -------- | -------------------------------------- | ------ |
| CORE-069 | Introduce Application Composition Root | Done   |
| CORE-070 | Add Application Acceptance Test        | Done   |
| CORE-071 | Update Project README                  | Done   |
| CORE-072 | Add Application Lifecycle Management   | Done   |

---

## Epic 8 — Evidence Provenance

| ID       | Story                                 | Status |
| -------- | ------------------------------------- | ------ |
| CORE-073 | Record Evidence Source                | Done   |
| CORE-074 | Update README for Evidence Provenance | Done   |

---

## Epic 9 — Evidence Relationships

| ID       | Story                                    | Status |
| -------- | ---------------------------------------- | ------ |
| CORE-075 | Classify Evidence Relationship           | Done   |
| CORE-076 | Update README for Evidence Relationships | Done   |

---

## Epic 10 — Project Continuity

| ID       | Story                   | Status |
| -------- | ----------------------- | ------ |
| CORE-077 | Refresh Project Context | Done   |

---

## Epic 11 — Aggregate Integrity

| ID       | Story                                               | Status |
| -------- | --------------------------------------------------- | ------ |
| CORE-078 | Protect Evidence Addition on Closed Investigations | Done   |
| CORE-079 | Protect Hypothesis Decisions on Closed Investigations | Done |

---

## Epic 12 — Development Reliability

| ID       | Story                              | Status |
| -------- | ---------------------------------- | ------ |
| CORE-080 | Close SQLite Test Resources        | Done   |
| CORE-081 | Reconcile CORE-080 Continuity      | Done   |

---

## Epic 13 — Investigation Integrity

| ID       | Story                          | Status |
| -------- | ------------------------------ | ------ |
| CORE-082 | Validate Investigation Purpose | Done   |

---

## Epic 14 — Developer Workflow

| ID       | Story                          | Status      |
| -------- | ------------------------------ | ----------- |
| CORE-083 | Add Safe Local Synchronization | Done        |

---

## Epic 15 — Documentation Continuity

| ID       | Story                           | Status      |
| -------- | ------------------------------- | ----------- |
| CORE-084 | Reconcile Project Documentation | Done        |

---

## Epic 16 — Hypothesis Integrity

| ID       | Story                                 | Status      |
| -------- | ------------------------------------- | ----------- |
| CORE-085 | Prevent Repeated Hypothesis Decisions | Done        |

---

## Epic 17 — Decision Integrity

| ID       | Story                                   | Status |
| -------- | --------------------------------------- | ------ |
| CORE-086 | Protect Decided Hypotheses from Removal | Done   |

---

## Epic 18 — Evidence-Basis Integrity

| ID       | Story                                            | Status |
| -------- | ------------------------------------------------ | ------ |
| CORE-087 | Protect Decided Hypotheses from Evidence Addition | Done  |

---

## Epic 19 — Persistence Integrity

| ID       | Story                                 | Status |
| -------- | ------------------------------------- | ------ |
| CORE-088 | Remove Orphaned SQLite Evidence       | Done   |

---

## Epic 20 — Schema Compatibility

| ID       | Story                                  | Status |
| -------- | -------------------------------------- | ------ |
| CORE-089 | Migrate Investigation Closure Schema   | Done   |

---

## Epic 21 — Event Store Compatibility

| ID       | Story                               | Status |
| -------- | ----------------------------------- | ------ |
| CORE-090 | Migrate Minimal Domain Event Schema | Done   |

---

## Epic 22 — Evidence Identity

| ID       | Story                     | Status |
| -------- | ------------------------- | ------ |
| CORE-091 | Prevent Duplicate Evidence | Done  |

---

## Epic 23 — Historical Traceability

| ID       | Story                                  | Status |
| -------- | -------------------------------------- | ------ |
| CORE-092 | Reject Unknown Persisted Domain Events | Done   |

---

## Epic 24 — Event Payload Integrity

| ID       | Story                                     | Status |
| -------- | ----------------------------------------- | ------ |
| CORE-093 | Validate Persisted Domain Event Payloads  | Done   |

---

## Epic 25 — Event Payload Diagnostics

| ID       | Story                                  | Status |
| -------- | -------------------------------------- | ------ |
| CORE-094 | Report Malformed Domain Event Payloads | Done   |

---

## Epic 26 — Evidence Ownership

| ID       | Story                                      | Status |
| -------- | ------------------------------------------ | ------ |
| CORE-095 | Prevent Cross-Hypothesis Evidence Reuse    | Done   |

---

## Epic 27 — Hypothesis Identity

| ID       | Story                                    | Status |
| -------- | ---------------------------------------- | ------ |
| CORE-096 | Reject Whitespace-Equivalent Hypotheses  | Done   |

---

## Epic 28 — Investigation Record Diagnostics

| ID       | Story                                  | Status |
| -------- | -------------------------------------- | ------ |
| CORE-097 | Report Malformed Investigation Records | Done   |

---

## Epic 29 — Hypothesis Record Diagnostics

| ID       | Story                               | Status |
| -------- | ----------------------------------- | ------ |
| CORE-098 | Report Malformed Hypothesis Records | Done   |

---

## Epic 30 — Evidence Record Diagnostics

| ID       | Story                             | Status |
| -------- | --------------------------------- | ------ |
| CORE-099 | Report Malformed Evidence Records | Done   |

---

## Epic 31 — Persisted Text Integrity

| ID       | Story                         | Status |
| -------- | ----------------------------- | ------ |
| CORE-100 | Validate Persisted Record Text | Done   |

---

## Epic 32 — Restored Aggregate Integrity

| ID       | Story                                 | Status |
| -------- | ------------------------------------- | ------ |
| CORE-101 | Reject Persisted Duplicate Hypotheses | Done   |

---

## Epic 33 — Restored Evidence Ownership

| ID       | Story                              | Status |
| -------- | ---------------------------------- | ------ |
| CORE-102 | Reject Restored Evidence Reuse     | Done   |

---

## Epic 34 — Claims

| ID       | Story                              | Status |
| -------- | ---------------------------------- | ------ |
| CORE-103 | Introduce Evidence-Grounded Claim  | Done   |
| CORE-104 | Attach Claims to Hypotheses        | Done   |
| CORE-105 | Route Claim Attachment Through Investigation | Done |
| CORE-106 | Persist Investigation Claims | Done |
| CORE-107 | Persist ClaimAdded Domain Event | Done |
| CORE-108 | Add Claim Use Case | Done |
| CORE-109 | Cover Claim Workflow Acceptance | Done |

---

## Epic 35 — Interpretations

| ID       | Story                   | Status |
| -------- | ----------------------- | ------ |
| CORE-110 | Introduce Interpretation | Done  |
| CORE-111 | Attach Interpretations to Hypotheses | Done |
| CORE-112 | Route Interpretation Through Investigation | Done |
| CORE-113 | Persist Investigation Interpretations | Done |
| CORE-114 | Persist InterpretationAdded Domain Event | Done |
| CORE-115 | Add Interpretation Use Case | Done |
| CORE-116 | Cover Interpretation Workflow Acceptance | Done |

---

## Epic 36 — Claim Ownership

| ID       | Story                                  | Status      |
| -------- | -------------------------------------- | ----------- |
| CORE-117 | Prevent Cross-Hypothesis Claim Reuse   | Done        |
| CORE-118 | Reject Restored Claim Reuse             | Done        |

## Epic 37 — Interpretation Ownership

| ID       | Story                                          | Status      |
| -------- | ---------------------------------------------- | ----------- |
| CORE-119 | Prevent Cross-Hypothesis Interpretation Reuse  | Done        |
| CORE-120 | Reject Restored Interpretation Reuse            | Done        |

## Epic 38 — Claim Record Diagnostics

| ID       | Story                          | Status      |
| -------- | ------------------------------ | ----------- |
| CORE-121 | Report Malformed Claim Records | Done        |

## Epic 39 — Interpretation Record Diagnostics

| ID       | Story                                   | Status      |
| -------- | --------------------------------------- | ----------- |
| CORE-122 | Report Malformed Interpretation Records | Done        |

## Epic 40 — Reasoning Record Text Integrity

| ID       | Story                              | Status      |
| -------- | ---------------------------------- | ----------- |
| CORE-123 | Validate Persisted Reasoning Text  | Done        |

## Epic 41 — Persisted Reasoning References

| ID       | Story                                               | Status |
| -------- | --------------------------------------------------- | ------ |
| CORE-124 | Reject Broken Persisted Claim References            | Done   |
| CORE-125 | Reject Broken Persisted Interpretation References   | Done   |

## Epic 42 — Thesis

| ID       | Story                         | Status      |
| -------- | ----------------------------- | ----------- |
| CORE-126 | Introduce Provisional Thesis  | Done        |
| CORE-127 | Attach Theses to Investigations | Done       |
| CORE-128 | Persist Investigation Theses   | Done         |
| CORE-129 | Persist ThesisAdded Domain Event | Done        |
| CORE-130 | Add Thesis Use Case             | Done          |
| CORE-131 | Cover Thesis Workflow Acceptance | Done         |
| CORE-132 | Cover Thesis Record Diagnostics  | Done          |
| CORE-133 | Reject Restored Duplicate Thesis Identities | Done |

## Current Story

No CORE story is currently active.

CORE-133 — Reject Restored Duplicate Thesis Identities is complete.

Aggregate restoration now has focused coverage proving duplicate thesis
identities are rejected while distinct identities restore without events.

CORE-133 validation passed 292 tests and the complete GitHub Actions quality gate.
