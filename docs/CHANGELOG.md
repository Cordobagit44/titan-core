# TITAN Core – Changelog

This document summarizes the functional evolution of TITAN Core.

It complements the Git history and the functional specifications by providing a concise overview of completed stories.

## CORE-146 — Preserve Assessment Timestamp in Domain Event

### Added

- Exact assessment `recorded_at` value on `AssessmentAdded`
- SQLite event payload persistence and reconstruction for the timestamp
- Legacy event migration with an explicit Unix-epoch timestamp marker
- Missing and malformed timestamp diagnostics with event and field context

### Changed

- Reconciled the public validated test count with the complete CI result

### Validation

- Assessment event timestamp tests — 4 passed
- pytest — 330 passed
- Ruff lint — passed
- Ruff format — passed
- mypy — passed
- GitHub Actions CI — passed

---

## CORE-145 — Record Assessment Timestamp

### Added

- Immutable UTC-aware `recorded_at` timestamp on narrative assessments
- Exact SQLite timestamp persistence and reconstruction
- Assessment-schema migration with an explicit Unix-epoch legacy marker
- Contextual diagnostics for malformed or timezone-naive persisted timestamps

### Architectural Notes

- The timestamp records when an assessment was formulated
- The public application call remains unchanged
- No verdict, score, confidence value, or automatic decision was introduced

### Validation

- Assessment timestamp domain and SQLite tests — 4 passed
- pytest — 326 passed
- Ruff lint — passed
- Ruff format — passed
- mypy — passed
- GitHub Actions CI — passed

---

## CORE-144 — Refresh README for Assessment Workflow

### Changed

- Public capability overview now includes narrative assessments
- End-to-end usage example now creates an assessment before investigation closure
- Domain, SQLite persistence, reconstruction, and use-case summaries include assessments
- Documented validated suite count updated to 321 tests

### Architectural Notes

- Assessments are documented as narrative evaluations without verdict or score
- Human judgment remains authoritative
- No production behavior, schema, API, or dependency changed

### Validation

- README assessment workflow review — passed
- pytest — 321 passed
- Ruff lint — passed
- Ruff format — passed
- mypy — passed
- GitHub Actions CI — passed

---

## CORE-143 — Reject Broken Persisted Assessment References

### Added

- Contextual SQLite rejection for assessments referencing unowned theses
- Persistence diagnostic identifying the damaged assessment record
- Focused regression coverage for well-formed but broken thesis references

### Architectural Notes

- The SQLite mapper translates aggregate referential integrity into record context
- Aggregate restoration remains authoritative for assessment ownership
- No schema, application API, domain event, or dependency changed

### Validation

- Broken assessment reference test — passed
- pytest — 321 passed
- Ruff lint — passed
- Ruff format — passed
- mypy — passed
- GitHub Actions CI — passed

---

## CORE-142 — Reject Restored Duplicate Assessment Identities

### Added

- Focused restoration coverage for duplicate assessment identities
- Positive restoration coverage for distinct assessments on one owned thesis
- Event-clean reconstruction assertion for restored assessment collections

### Architectural Notes

- Assessment identity, not narrative equality, defines duplication
- Aggregate restoration remains the uniqueness enforcement boundary
- No production behavior, persistence schema, or public API changed

### Validation

- Restored assessment identity tests — 2 passed
- pytest — 320 passed
- Ruff lint — passed
- Ruff format — passed
- mypy — passed
- GitHub Actions CI — passed

---

## CORE-141 — Cover Assessment Record Diagnostics

### Added

- Focused SQLite reconstruction tests for malformed assessment identifiers
- Contextual diagnostic coverage for invalid assessment thesis references
- Contextual diagnostic coverage for blank persisted assessment narratives

### Architectural Notes

- Existing persistence-boundary behavior is locked down without production changes
- Diagnostics identify the damaged record and field where identity is available
- Assessment semantics and public application APIs remain unchanged

### Validation

- Assessment record diagnostics tests — 3 passed
- pytest — 318 passed
- Ruff lint — passed
- Ruff format — passed
- mypy — passed
- GitHub Actions CI — passed

---

## CORE-140 — Cover Assessment Workflow Acceptance

### Added

- Narrative assessment creation in the composed SQLite-backed acceptance workflow
- Restart assertions for assessment identity, thesis reference, and narrative
- Listing assertion for the reconstructed assessment collection

### Architectural Notes

- Coverage uses only the public `TitanApplication` surface
- No production behavior, schema, API, or dependency changed
- Assessments remain narrative evaluations without verdict or numeric confidence

### Validation

- Assessment-enabled acceptance workflow — passed
- pytest — 315 passed
- Ruff lint — passed
- Ruff format — passed
- mypy — passed
- GitHub Actions CI — passed

---

## CORE-139 — Add Assessment Use Case

### Added

- Transactional `AddAssessment` application use case
- Atomic aggregate and `AssessmentAdded` persistence through Unit of Work
- `add_assessment` exposure from `TitanApplication` and `bootstrap()`
- Rollback coverage for missing investigation, unknown thesis, and event failure

### Architectural Notes

- The application creates assessments and coordinates persistence
- The investigation remains authoritative for thesis ownership and lifecycle
- Verdicts, scores, and interfaces remain unchanged

### Validation

- AddAssessment tests — 4 passed
- pytest — 315 passed
- Ruff lint — passed
- Ruff format — passed
- mypy — passed
- GitHub Actions CI — passed

---

## CORE-138 — Persist AssessmentAdded Domain Event

### Added

- Nullable `assessment_id` event-schema storage and safe migration
- SQLite serialization and reconstruction of `AssessmentAdded`
- Contextual missing-field and malformed-UUID diagnostics

### Architectural Notes

- Event history stores investigation, assessment, and thesis identity only
- Aggregate persistence remains the source of narrative content
- Application orchestration remains unchanged

### Validation

- Assessment event persistence tests — 4 passed
- pytest — 311 passed
- Ruff lint — passed
- Ruff format — passed
- mypy — passed
- GitHub Actions CI — passed

---

## CORE-137 — Persist Investigation Assessments

### Added

- SQLite `assessments` table beneath investigations and theses
- Assessment identity, ownership, thesis-reference, narrative, and order persistence
- Event-clean reconstruction through `Investigation.restore()`
- Safe replacement of assessment rows on aggregate re-save

### Architectural Notes

- Assessments reconstruct after theses to preserve reference validation
- Aggregate restoration enforces assessment identity and thesis ownership
- Event-store and application APIs remain unchanged

### Validation

- Assessment persistence tests — 3 passed
- pytest — 307 passed
- Ruff lint — passed
- Ruff format — passed
- mypy — passed
- GitHub Actions CI — passed

---

## CORE-136 — Attach Assessments to Investigations

### Added

- Investigation ownership of narrative assessments
- Owned-thesis reference validation
- Immutable tuple exposure through `Investigation.assessments`
- `AssessmentAdded` with investigation, assessment, and thesis identities
- Duplicate identity and closed-investigation protections

### Architectural Notes

- The investigation owns both evaluated theses and their assessments
- Equal narratives remain distinct through explicit identity
- Persistence and application APIs remain intentionally unchanged

### Validation

- Assessment ownership domain tests — 7 passed
- pytest — 304 passed
- Ruff lint — passed
- Ruff format — passed
- mypy — passed
- GitHub Actions CI — passed

---

## CORE-135 — Introduce Narrative Assessment

### Added

- Immutable UUID-backed `AssessmentId`
- Immutable narrative `Assessment` linked to one `ThesisId`
- Non-blank narrative validation and explicit identity reconstruction

### Architectural Notes

- Assessment begins as explainable narrative evaluation
- Categorical verdicts and numeric confidence remain intentionally absent
- Ownership, persistence, events, and application APIs remain undefined

### Validation

- Assessment domain tests — 5 passed
- pytest — 297 passed
- Ruff lint — passed
- Ruff format — passed
- mypy — passed
- GitHub Actions CI — passed

---

## CORE-134 — Refresh README for Thesis Workflow

### Changed

- Documented investigation-owned provisional theses
- Added `add_thesis` application usage and exposed-use-case listing
- Expanded SQLite and restart reconstruction descriptions through theses
- Updated the validated suite count to 292 tests

### Architectural Notes

- README examples use only the public composed application surface
- No production behavior, schema, API, test, or dependency changed

### Validation

- pytest — 292 passed
- Ruff lint — passed
- Ruff format — passed
- mypy — passed
- GitHub Actions CI — passed

---

## CORE-133 — Reject Restored Duplicate Thesis Identities

### Changed

- Covered duplicate thesis identity rejection during aggregate restoration
- Confirmed distinct thesis identities restore without pending events

### Architectural Notes

- Restored aggregate integrity matches live thesis mutation rules
- No production behavior, schema, API, or dependency changed

### Validation

- Restored thesis identity tests — 2 passed
- pytest — 292 passed
- Ruff lint — passed
- Ruff format — passed
- mypy — passed
- GitHub Actions CI — passed

---

## CORE-132 — Cover Thesis Record Diagnostics

### Changed

- Covered malformed persisted thesis identity diagnostics
- Covered blank persisted thesis statements with thesis and field context

### Architectural Notes

- Validation remains at the SQLite deserialization boundary
- No production behavior, schema, API, or dependency changed

### Validation

- Thesis record diagnostic tests — 2 passed
- pytest — 290 passed
- Ruff lint — passed
- Ruff format — passed
- mypy — passed
- GitHub Actions CI — passed

---

## CORE-131 — Cover Thesis Workflow Acceptance

### Changed

- Extended the composed investigation workflow with thesis creation
- Verified thesis identity and statement after SQLite-backed restart
- Verified listed investigations preserve the same reconstructed thesis

### Architectural Notes

- Coverage uses only the public `TitanApplication` surface
- No production behavior, schema, API, or dependency changed

### Validation

- Thesis-enabled acceptance workflow — passed
- pytest — 288 passed
- Ruff lint — passed
- Ruff format — passed
- mypy — passed
- GitHub Actions CI — passed

---

## CORE-130 — Add Thesis Use Case

### Added

- Transactional `AddThesis` application use case
- Atomic aggregate and `ThesisAdded` persistence through Unit of Work
- `add_thesis` exposure from `TitanApplication` and `bootstrap()`
- Rollback coverage for missing, closed, and persistence-failure paths

### Architectural Notes

- The application creates the thesis and coordinates persistence
- The investigation remains responsible for lifecycle and identity invariants
- Selection, assessment, synthesis, and interfaces remain unchanged

### Validation

- AddThesis tests — 4 passed
- pytest — 288 passed
- Ruff lint — passed
- Ruff format — passed
- mypy — passed
- GitHub Actions CI — passed

---

## CORE-129 — Persist ThesisAdded Domain Event

### Added

- Nullable `thesis_id` event-schema storage and safe migration
- SQLite serialization and reconstruction of `ThesisAdded`
- Contextual missing-field and malformed-UUID diagnostics

### Architectural Notes

- Event history stores investigation and thesis identity only
- Aggregate persistence remains the source of thesis statements
- Application orchestration remains unchanged

### Validation

- Thesis event persistence tests — 4 passed
- pytest — 284 passed
- Ruff lint — passed
- Ruff format — passed
- mypy — passed
- GitHub Actions CI — passed

---

## CORE-128 — Persist Investigation Theses

### Added

- SQLite `theses` table beneath the owning investigation
- Thesis identity, statement, ownership, and insertion-order persistence
- Aggregate restoration of theses without pending mutation events
- Safe replacement of prior thesis rows on aggregate re-save

### Architectural Notes

- Theses remain direct investigation-owned state
- Persistence reconstructs through `Investigation.restore()`
- Application APIs and domain-event persistence remain unchanged

### Validation

- Thesis persistence tests — 3 passed
- pytest — 280 passed
- Ruff lint — passed
- Ruff format — passed
- mypy — passed
- GitHub Actions CI — passed

---

## CORE-127 — Attach Theses to Investigations

### Added

- Investigation ownership of provisional theses
- Immutable tuple exposure through `Investigation.theses`
- `ThesisAdded` domain event containing investigation and thesis identities
- Duplicate thesis identity and closed-investigation mutation protection

### Architectural Notes

- Thesis ownership remains inside the investigation aggregate
- Equal statements remain valid when thesis identities differ
- Persistence and application APIs remain intentionally unchanged

### Validation

- Thesis ownership domain tests — 5 passed
- pytest — 277 passed
- Ruff lint — passed
- Ruff format — passed
- mypy — passed
- GitHub Actions CI — passed

---

## CORE-126 — Introduce Provisional Thesis

### Added

- Immutable `ThesisId` identity value
- Immutable provisional `Thesis` domain model
- Non-blank thesis statement validation and explicit identity reconstruction

### Architectural Notes

- Thesis begins as a domain-neutral conclusion value
- Aggregate ownership, grounding, persistence, status, and assessment remain
  intentionally undefined
- No public API, schema, event type, or dependency changed

### Validation

- Thesis domain tests — 4 passed
- pytest — 272 passed
- Ruff lint — passed
- Ruff format — 220 files already formatted
- mypy — 79 source files checked

---

## CORE-125 — Reject Broken Persisted Interpretation References

### Changed

- Persisted interpretations referencing claims outside their hypothesis are
  rejected
- The rejection identifies the interpretation and missing claim relationship
- The original domain lookup failure remains available through exception
  chaining

### Architectural Notes

- Reference validation remains at the SQLite reconstruction boundary
- Valid interpretation grounding and aggregate behavior remain unchanged
- No public API, schema, event type, or dependency changed

### Validation

- Targeted SQLite investigation repository test — passed
- pytest — 268 passed
- Ruff lint — passed
- Ruff format — 217 files already formatted
- mypy — 77 source files checked

---

## CORE-124 — Reject Broken Persisted Claim References

### Changed

- Persisted claims referencing evidence outside their hypothesis are rejected
- The rejection identifies the claim and missing evidence relationship
- The original domain lookup failure remains available through exception
  chaining

### Architectural Notes

- Reference validation remains at the SQLite reconstruction boundary
- Valid claim grounding and aggregate behavior remain unchanged
- No public API, schema, event type, or dependency changed

### Validation

- Targeted SQLite investigation repository test — passed
- pytest — 267 passed
- Ruff lint — passed
- Ruff format — 216 files already formatted
- mypy — 77 source files checked

---

## CORE-123 — Validate Persisted Reasoning Text

### Changed

- Blank persisted claim statements now raise contextual deserialization errors
- Blank persisted interpretation rationales now raise contextual
  deserialization errors
- Existing required-text validation now covers every current reasoning record

### Architectural Notes

- Validation remains at the SQLite deserialization boundary
- Valid claim and interpretation reconstruction remains unchanged
- No public API, schema, event type, or dependency changed

### Validation

- Parameterized persisted text tests — passed
- pytest — 266 passed
- Ruff lint — passed
- Ruff format — 215 files already formatted
- mypy — 77 source files checked

---

## CORE-122 — Report Malformed Interpretation Records

### Changed

- Malformed persisted interpretation identifiers now raise contextual
  deserialization errors
- Malformed persisted interpretation claim identifiers identify the owning
  interpretation and invalid field
- Original UUID parser failures remain available through exception chaining

### Architectural Notes

- Validation remains at the SQLite deserialization boundary
- Valid interpretation reconstruction and aggregate ownership behavior remain
  unchanged
- No public API, schema, event type, or dependency changed

### Validation

- Targeted SQLite investigation repository tests — passed
- pytest — 264 passed
- Ruff lint — passed
- Ruff format — 214 files already formatted
- mypy — 77 source files checked

---

## CORE-121 — Report Malformed Claim Records

### Changed

- Malformed persisted claim identifiers now raise contextual deserialization
  errors
- Malformed persisted claim evidence identifiers identify the owning claim and
  invalid field
- Original UUID parser failures remain available through exception chaining

### Architectural Notes

- Validation remains at the SQLite deserialization boundary
- Valid claim reconstruction and aggregate ownership behavior remain unchanged
- No public API, schema, event type, or dependency changed

### Validation

- Targeted SQLite investigation repository tests — passed
- pytest — 262 passed
- Ruff lint — passed
- Ruff format — 213 files already formatted
- mypy — 77 source files checked

---

## CORE-120 — Reject Restored Interpretation Reuse

### Changed

- Investigation restoration rejects interpretation identifiers reused across
  hypotheses
- Rejection uses the established aggregate ownership error
- Valid restored interpretation state remains unchanged

### Architectural Notes

- Interpretation identity ownership is enforced consistently for mutation and
  restoration
- SQLite behavior remains unchanged because interpretation identifiers are
  already primary keys
- No public API, schema, event type, or dependency changed

### Validation

- Targeted investigation restoration tests — passed
- pytest — 260 passed
- Ruff lint — passed
- Ruff format — 212 files already formatted
- mypy — 77 source files checked

---

## CORE-119 — Prevent Cross-Hypothesis Interpretation Reuse

### Changed

- Investigation-level interpretation attachment rejects identifiers already
  owned by another hypothesis
- Rejected reuse leaves the target hypothesis unchanged and emits no event
- Distinct interpretation identities remain valid under existing hypothesis
  rules

### Architectural Notes

- Interpretation identity ownership is enforced at the aggregate boundary
- Hypothesis-level reference and duplicate checks remain unchanged
- No schema, persistence, application API, event payload, or dependency changed

### Validation

- Targeted investigation interpretation tests — passed
- pytest — 259 passed
- Ruff lint — passed
- Ruff format — 211 files already formatted
- mypy — 77 source files checked

---

## CORE-118 — Reject Restored Claim Reuse

### Changed

- Investigation restoration rejects claim identifiers reused across hypotheses
- Rejection uses the established aggregate ownership error
- Valid restored claim state remains unchanged

### Architectural Notes

- Claim identity ownership is enforced consistently for mutation and restoration
- SQLite behavior remains unchanged because claim identifiers are already primary keys
- No public API, schema, event type, or dependency changed

### Validation

- Targeted investigation restoration tests — passed
- pytest — 258 passed
- Ruff lint — passed
- Ruff format — 210 files already formatted
- mypy — 77 source files checked

---

## CORE-117 — Prevent Cross-Hypothesis Claim Reuse

### Changed

- Investigation-level claim attachment rejects identifiers already owned by another hypothesis
- Rejected reuse leaves the target hypothesis unchanged and emits no event
- Distinct claim identities remain valid under existing hypothesis rules

### Architectural Notes

- Claim identity ownership is enforced at the aggregate boundary
- Hypothesis-level grounding and duplicate checks remain unchanged
- No schema, persistence, application API, or event payload changed

### Validation

- Targeted investigation claim tests — passed
- pytest — 257 passed
- Ruff lint — passed
- Ruff format — 209 files already formatted
- mypy — 77 source files checked

---

## CORE-116 — Cover Interpretation Workflow Acceptance

### Changed

- The complete application workflow now creates an explicit interpretation
- Application restart coverage verifies interpretation identity, rationale, claim reference, and hypothesis reference
- Existing investigation, hypothesis, evidence, claim, decision, and closure coverage remains

### Architectural Notes

- Acceptance uses only the public `TitanApplication` surface
- A real SQLite database is closed and reopened during verification
- No production behavior, schema, API, or dependency changed

### Validation

- Interpretation-enabled acceptance workflow — passed
- pytest — 256 passed
- Ruff lint — passed
- Ruff format — 208 files already formatted
- mypy — 77 source files checked

---

## CORE-115 — Add Interpretation Use Case

### Added

- Transactional `AddInterpretation` application use case
- `add_interpretation` exposure from `TitanApplication` and `bootstrap()`
- Application usage documentation for explicit claim interpretation

### Changed

- Interpretation aggregate state and `InterpretationAdded` persist in one Unit of Work
- Failed interpretation operations roll back without committing

### Architectural Notes

- The application creates interpretations while the aggregate enforces ownership and lifecycle invariants
- No automatic interpretation, scoring, HTTP, CLI, or AI integration was introduced

### Validation

- Targeted AddInterpretation and bootstrap tests — passed
- pytest — 256 passed
- Ruff lint — passed
- Ruff format — 207 files already formatted
- mypy — 77 source files checked

---

## CORE-114 — Persist InterpretationAdded Domain Event

### Added

- SQLite serialization and reconstruction for `InterpretationAdded`
- Event-store schema migration for interpretation identifiers
- Missing and malformed interpretation identifier diagnostics

### Changed

- Interpretation events preserve hypothesis, interpretation, and claim identity

### Architectural Notes

- The event store records interpretation lineage while aggregate persistence owns rationale
- Existing event histories migrate through the established copy-and-replace path
- No application API was introduced

### Validation

- Targeted SQLite domain event repository tests — 27 passed
- pytest — 252 passed
- Ruff lint — passed
- Ruff format — 204 files already formatted
- mypy — 75 source files checked

---

## CORE-113 — Persist Investigation Interpretations

### Added

- SQLite interpretation records with hypothesis and claim references
- Aggregate restoration of interpretations for `get()` and `list()`

### Changed

- Aggregate replacement deletes interpretation rows before their claims
- Reconstruction restores evidence, claims, and then interpretations

### Architectural Notes

- Interpretations remain inside the hypothesis-owned aggregate boundary
- Domain validation is reused during restoration and generated events are cleared
- No application API was introduced

### Validation

- Targeted SQLite investigation repository tests — 29 passed
- pytest — 249 passed
- Ruff lint — passed
- Ruff format — 203 files already formatted
- mypy — 75 source files checked

---

## CORE-112 — Route Interpretation Through Investigation

### Added

- `Investigation.add_interpretation()` aggregate operation
- Aggregate lookup and delegation to the selected hypothesis

### Changed

- Closed investigations reject interpretation attachment before mutation
- Unknown hypothesis identifiers are rejected consistently

### Architectural Notes

- Investigation owns lifecycle and lookup protections
- Hypothesis retains interpretation reference, identity, and state invariants
- No persistence or application API was introduced

### Validation

- Targeted investigation interpretation tests — 3 passed
- pytest — 247 passed
- Ruff lint — passed
- Ruff format — 202 files already formatted
- mypy — 75 source files checked

---

## CORE-111 — Attach Interpretations to Hypotheses

### Added

- Immutable interpretation collection owned by `Hypothesis`
- Hypothesis and claim reference validation before attachment
- `InterpretationAdded` event preserving all reasoning identities

### Changed

- Decided hypotheses reject new interpretations
- Duplicate interpretation identities are rejected without mutation or events

### Architectural Notes

- Hypothesis owns evidence, claims, and interpretations in one reasoning boundary
- Equal rationale does not collapse distinct interpretation identities
- No persistence or application API was introduced

### Validation

- Targeted hypothesis interpretation tests — 8 passed
- pytest — 244 passed
- Ruff lint — passed
- Ruff format — 200 files already formatted
- mypy — 74 source files checked

---

## CORE-110 — Introduce Interpretation

### Added

- Immutable `Interpretation` domain model
- Generated and restorable `InterpretationId`
- Explicit claim, hypothesis, and non-blank rationale fields

### Architectural Notes

- One interpretation connects one claim to one hypothesis
- Multiple reasoning links can compose without introducing a graph prematurely
- No ownership, persistence, event, application API, or AI behavior was added

### Validation

- Targeted interpretation domain tests — 4 passed
- pytest — 236 passed
- Ruff lint — passed
- Ruff format — 198 files already formatted
- mypy — 73 source files checked

---

## CORE-109 — Cover Claim Workflow Acceptance

### Changed

- The complete application workflow now creates an evidence-grounded claim
- Application restart coverage verifies claim identity, statement, and provenance
- Existing investigation, hypothesis, evidence, decision, and closure coverage remains

### Architectural Notes

- Acceptance uses only the public `TitanApplication` surface
- A real SQLite database is closed and reopened during verification
- No production behavior, schema, API, or dependency changed

### Validation

- Claim-enabled acceptance workflow — 1 passed
- pytest — 232 passed
- Ruff lint — passed
- Ruff format — 195 files already formatted
- mypy — 71 source files checked

---

## CORE-108 — Add Claim Use Case

### Added

- Transactional `AddClaim` application use case
- `add_claim` exposure from `TitanApplication` and `bootstrap()`
- Application usage documentation for evidence-grounded claims

### Changed

- Claim aggregate state and `ClaimAdded` persist in one Unit of Work
- All failed claim operations roll back and do not commit

### Architectural Notes

- Application creates claims while the aggregate enforces domain invariants
- Unit of Work coordinates investigation and domain-event repositories
- No HTTP, CLI, automatic extraction, or AI integration was introduced

### Validation

- Targeted AddClaim and bootstrap tests — 7 passed
- pytest — 232 passed
- Ruff lint — passed
- Ruff format — 194 files already formatted
- mypy — 71 source files checked

---

## CORE-107 — Persist ClaimAdded Domain Event

### Added

- Nullable `claim_id` column in the SQLite event schema
- `ClaimAdded` serialization and ordered reconstruction
- Required-field and malformed-UUID diagnostics for claim events

### Changed

- Legacy event tables migrate while preserving existing rows
- Hypothesis and evidence identities are stored alongside claim identity

### Architectural Notes

- The domain-event store remains append-only and backward-compatible
- Existing event types retain their payload shapes
- No application use case or automatic extraction was introduced

### Validation

- Targeted SQLite domain-event repository tests — 24 passed
- pytest — 228 passed
- Ruff lint — passed
- Ruff format — 191 files already formatted
- mypy — 69 source files checked

---

## CORE-106 — Persist Investigation Claims

### Added

- SQLite `claims` table beneath hypothesis ownership
- Claim save and ordered reconstruction in `get()` and `list()`
- Preservation of `ClaimId`, statement, and `EvidenceId`

### Changed

- Aggregate replacement removes previous claim rows before owner rows
- Evidence is restored before claims so provenance is revalidated

### Architectural Notes

- Claim state is part of investigation aggregate persistence
- Restored `ClaimAdded` events are cleared with other reconstruction events
- No application use case or event-store serialization was introduced

### Validation

- Targeted SQLite investigation repository tests — 27 passed
- pytest — 225 passed
- Ruff lint — passed
- Ruff format — 190 files already formatted
- mypy — 69 source files checked

---

## CORE-105 — Route Claim Attachment Through Investigation

### Added

- `Investigation.add_claim()` aggregate operation
- Aggregate lookup and delegation to the selected hypothesis

### Changed

- Closed investigations reject claim attachment before mutation
- Unknown hypothesis identifiers are rejected consistently

### Architectural Notes

- Investigation owns lifecycle and lookup protections
- Hypothesis retains claim provenance, identity, and decision-state invariants
- No application use case or persistence was introduced

### Validation

- Targeted investigation claim tests — 3 passed
- pytest — 223 passed
- Ruff lint — passed
- Ruff format — 189 files already formatted
- mypy — 69 source files checked

---

## CORE-104 — Attach Claims to Hypotheses

### Added

- Immutable claim collection owned by `Hypothesis`
- Evidence-membership validation before claim attachment
- `ClaimAdded` event preserving hypothesis, claim, and evidence identities

### Changed

- Decided hypotheses reject new claims
- Duplicate claim identities are rejected without mutation or events

### Architectural Notes

- Claim ownership follows the existing hypothesis evidence boundary
- Statement equality does not collapse distinct claim identities
- No persistence or application API was introduced

### Validation

- Targeted hypothesis claim tests — 7 passed
- pytest — 220 passed
- Ruff lint — passed
- Ruff format — 187 files already formatted
- mypy — 68 source files checked

---

## CORE-103 — Introduce Evidence-Grounded Claim

### Added

- Immutable `Claim` domain model with a non-blank statement
- Generated and restorable `ClaimId`
- Explicit `EvidenceId` provenance link on every claim

### Architectural Notes

- Claims remain domain-neutral and separate from evidence descriptions
- No aggregate integration, persistence, event, or application API was added
- No AI provider or automatic extraction behavior was introduced

### Validation

- Targeted claim domain tests — 4 passed
- pytest — 213 passed
- Ruff lint — passed
- Ruff format — 185 files already formatted
- mypy — 67 source files checked

---

## CORE-102 — Reject Restored Evidence Reuse

### Changed

- Investigation restoration rejects evidence IDs reused across hypotheses
- Rejection uses the established aggregate ownership error
- Distinct restored evidence identities remain unchanged

### Architectural Notes

- Evidence ownership is enforced consistently for mutation and restoration
- SQLite behavior remains unchanged because evidence IDs are already primary keys
- No public signature, schema, event type, or dependency changed

### Validation

- Targeted investigation domain tests — 35 passed
- pytest — 209 passed
- Ruff lint — passed
- Ruff format — 182 files already formatted
- mypy — 65 source files checked

---

## CORE-101 — Reject Persisted Duplicate Hypotheses

### Changed

- Investigation restoration rejects exact duplicate hypothesis statements
- Leading and trailing whitespace cannot bypass uniqueness during restoration
- Case-distinct statements remain valid and restored text remains unchanged

### Architectural Notes

- Statement uniqueness is enforced consistently for mutation and restoration
- Rejection occurs before a restored aggregate can emit or expose state
- No public signature, schema, event type, or dependency changed

### Validation

- Targeted domain and SQLite repository tests — 59 passed
- pytest — 208 passed
- Ruff lint — passed
- Ruff format — 181 files already formatted
- mypy — 65 source files checked

---

## CORE-100 — Validate Persisted Record Text

### Changed

- Blank persisted investigation titles and purposes are rejected contextually
- Blank persisted hypothesis statements are rejected contextually
- Blank persisted evidence descriptions and sources are rejected contextually

### Architectural Notes

- Required text is validated at the SQLite deserialization boundary
- Valid text is preserved exactly; no normalization or rewriting occurs
- No public signature, schema, event type, or dependency changed

### Validation

- Targeted SQLite investigation repository tests — 24 passed
- pytest — 204 passed
- Ruff lint — passed
- Ruff format — 180 files already formatted
- mypy — 65 source files checked

---

## CORE-099 — Report Malformed Evidence Records

### Changed

- Malformed persisted evidence identifiers now identify the invalid field
- Malformed evidence relationships now identify both the evidence and field
- Original UUID and enum parser failures remain chained as causes

### Architectural Notes

- Parsing diagnostics remain private to the SQLite deserialization boundary
- Existing saving, ordering, migration, and valid restoration behavior remains unchanged
- No public signature, schema, event type, or dependency changed

### Validation

- Targeted SQLite investigation repository tests — 19 passed
- pytest — 199 passed
- Ruff lint — passed
- Ruff format — 179 files already formatted
- mypy — 65 source files checked

---

## CORE-098 — Report Malformed Hypothesis Records

### Changed

- Malformed persisted hypothesis identifiers now identify the invalid field
- Malformed persisted hypothesis statuses now identify both the hypothesis and field
- Original UUID and enum parser failures remain chained as causes

### Architectural Notes

- Parsing diagnostics remain private to the SQLite deserialization boundary
- Existing saving, ordering, migration, and valid restoration behavior remains unchanged
- No public signature, schema, event type, or dependency changed

### Validation

- Targeted SQLite investigation repository tests — 17 passed
- pytest — 197 passed
- Ruff lint — passed
- Ruff format — 178 files already formatted
- mypy — 65 source files checked

---

## CORE-097 — Report Malformed Investigation Records

### Changed

- Malformed persisted investigation identifiers now identify the invalid field
- Malformed persisted statuses and closure timestamps now identify both the investigation and field
- Original UUID, enum, and datetime parser failures remain chained as causes

### Architectural Notes

- Parsing diagnostics remain private to the SQLite deserialization boundary
- Existing saving, ordering, migration, and valid restoration behavior remains unchanged
- No public signature, schema, event type, or dependency changed

### Validation

- Targeted SQLite investigation repository tests — 15 passed
- pytest — 195 passed
- Ruff lint — passed
- Ruff format — 177 files already formatted
- mypy — 65 source files checked

---

## CORE-096 — Reject Whitespace-Equivalent Hypotheses

### Changed

- Leading and trailing whitespace no longer bypass hypothesis duplicate detection
- Rejected duplicates add no hypothesis and emit no `HypothesisAdded` event
- Application rejection rolls back and does not commit
- Accepted statement text remains unchanged and comparison remains case-sensitive

### Architectural Notes

- Trimmed text is used only for aggregate uniqueness comparison
- `Hypothesis` continues to preserve the supplied validated statement
- No public signature, schema, event type, or dependency changed

### Validation

- Targeted investigation and add-hypothesis tests — 37 passed
- pytest — 192 passed
- Ruff lint — passed
- Ruff format — 176 files already formatted
- mypy — 65 source files checked

---

## CORE-095 — Prevent Cross-Hypothesis Evidence Reuse

### Changed

- An evidence identifier can belong to only one hypothesis in an investigation
- Rejected cross-hypothesis reuse leaves both evidence collections unchanged
- Rejected reuse emits no new `EvidenceAdded` event

### Architectural Notes

- Cross-hypothesis ownership remains an `Investigation` aggregate invariant
- Local duplicate and decision-state protections remain inside `Hypothesis`
- No public signature, schema, event type, or dependency changed

### Validation

- Targeted investigation evidence tests — 4 passed
- pytest — 189 passed
- Ruff lint — passed
- Ruff format — 175 files already formatted
- mypy — 65 source files checked

---

## CORE-094 — Report Malformed Domain Event Payloads

### Changed

- Malformed persisted UUIDs now identify their event type and payload field
- Malformed closure timestamps now identify their event type and field
- Original UUID and datetime parser failures remain chained as causes

### Architectural Notes

- Parsing diagnostics remain private to the SQLite deserialization boundary
- Missing-field, unknown-type, saving, ordering, and migration behavior remain unchanged
- No public signature, schema, event type, or dependency changed

### Validation

- Targeted SQLite domain-event repository tests — 21 passed
- pytest — 188 passed
- Ruff lint — passed
- Ruff format — 174 files already formatted
- mypy — 65 source files checked

---

## CORE-093 — Validate Persisted Domain Event Payloads

### Changed

- Required payload fields are validated before supported events are reconstructed
- Incomplete events now raise a `ValueError` naming the event type and field
- Investigation, closure, hypothesis, and evidence payload shapes are covered

### Architectural Notes

- Validation remains private to the SQLite deserialization boundary
- Saving, ordering, migration, and unknown-type behavior remain unchanged
- No public signature, schema, event type, or dependency changed

### Validation

- Targeted SQLite domain-event repository tests — 17 passed
- pytest — 184 passed
- Ruff lint — passed
- Ruff format — 173 files already formatted
- mypy — 65 source files checked

---

## CORE-092 — Reject Unknown Persisted Domain Events

### Changed

- Reading an unknown persisted event type now raises an explicit `ValueError`
- Unknown event rows are no longer silently omitted from returned history
- All supported event reconstruction and ordering remain unchanged

### Architectural Notes

- Explicit deserialization failure remains inside the SQLite event repository
- No public signature, schema, event type, or dependency changed

### Validation

- Targeted SQLite domain-event repository tests — 13 passed
- pytest — 180 passed
- Ruff lint — passed
- Ruff format — 172 files already formatted
- mypy — 65 source files checked

---

## CORE-091 — Prevent Duplicate Evidence

### Changed

- A hypothesis now rejects an evidence identifier already in its collection
- Rejected duplicates leave evidence unchanged and emit no `EvidenceAdded` event
- Distinct evidence identifiers remain valid when descriptive fields match

### Architectural Notes

- Evidence identity protection remains inside `Hypothesis`
- Duplicate detection uses `EvidenceId`, not description or source text
- No public API, schema, event type, or dependency changed

### Validation

- Targeted hypothesis tests — 20 passed
- pytest — 179 passed
- Ruff lint — passed
- Ruff format — 171 files already formatted
- mypy — 65 source files checked

---

## CORE-090 — Migrate Minimal Domain Event Schema

### Changed

- Minimal historical domain-event tables now migrate to the current schema
- Missing optional payload columns are copied as `NULL`
- Existing events keep their identifiers, order, and available payload
- Migrated tables accept current hypothesis and evidence events

### Architectural Notes

- Migration continues to rebuild the event table transactionally
- No public API, domain rule, event type, or dependency changed

### Validation

- Targeted SQLite domain-event repository tests — 12 passed
- pytest — 177 passed
- Ruff lint — passed
- Ruff format — 170 files already formatted
- mypy — 65 source files checked

---

## CORE-089 — Migrate Investigation Closure Schema

### Changed

- Legacy SQLite `investigations` tables now receive a nullable `closed_at`
  column automatically
- Existing investigation rows and identifiers remain unchanged
- Legacy rows restore with no invented closure timestamp

### Architectural Notes

- Migration is additive and idempotent
- No public API, domain rule, event type, or dependency changed

### Validation

- Targeted SQLite investigation repository tests — 12 passed
- pytest — 176 passed
- Ruff lint — passed
- Ruff format — 169 files already formatted
- mypy — 65 source files checked

---

## CORE-088 — Remove Orphaned SQLite Evidence

### Changed

- SQLite saves now remove evidence for all previously persisted hypotheses of
  the investigation before replacing those hypotheses
- Removing and saving a hypothesis no longer leaves orphaned evidence rows
- Evidence belonging to other investigations remains untouched

### Architectural Notes

- Cleanup remains inside the repository's existing transaction boundary
- No public API, domain rule, schema, event type, or dependency changed

### Validation

- Targeted SQLite investigation repository tests — 11 passed
- pytest — 175 passed
- Ruff lint — passed
- Ruff format — 168 files already formatted
- mypy — 65 source files checked

---

## CORE-087 — Protect Decided Hypotheses from Evidence Addition

### Changed

- Confirmed hypotheses can no longer accept new evidence
- Rejected hypotheses can no longer accept new evidence
- Pending hypotheses continue to accept evidence
- Failed additions leave evidence unchanged and emit no `EvidenceAdded` event
- Application failures roll back and do not commit

### Architectural Notes

- Evidence-collection protection remains inside `Hypothesis`
- No persistence schema, event type, or dependency changed

### Validation

- Targeted hypothesis and evidence-addition tests — 30 passed
- pytest — 174 passed
- Ruff lint — passed
- Ruff format — 167 files already formatted
- mypy — 65 source files checked

---

## CORE-086 — Protect Decided Hypotheses from Removal

### Changed

- Confirmed hypotheses can no longer be removed from an investigation
- Rejected hypotheses can no longer be removed from an investigation
- Pending hypotheses remain removable
- Failed removals leave aggregate membership unchanged and emit no removal event
- Application failures roll back and do not commit

### Architectural Notes

- Aggregate-membership protection remains inside `Investigation`
- No persistence schema, event type, or dependency changed

### Validation

- Targeted hypothesis-removal tests — 13 passed
- pytest — 170 passed
- Ruff lint — passed
- Ruff format — 166 files already formatted
- mypy — 65 source files checked

---

## CORE-085 — Prevent Repeated Hypothesis Decisions

### Changed

- Confirming an already confirmed hypothesis now raises a domain error
- Rejecting an already rejected hypothesis now raises a domain error
- Failed repeated decisions emit no additional domain event
- Application failures roll back and do not commit

### Architectural Notes

- The invariant remains inside `Hypothesis`
- Existing opposite-terminal transition protections remain unchanged
- No persistence schema, event type, or dependency changed

### Validation

- Targeted hypothesis decision tests — 30 passed
- pytest — 166 passed
- Ruff lint — passed
- Ruff format — 165 files already formatted
- mypy — 65 source files checked

---

## CORE-084 — Reconcile Project Documentation

### Changed

- Reconciled the README test count and investigation-purpose capability
- Added missing changelog coverage through CORE-083
- Refreshed the current development state and next-step continuity guidance
- Recorded CORE-084 in the backlog

### Architectural Notes

- Documentation-only continuity repair
- No production, test, persistence, or dependency behavior changed
- No future reasoning concept was accepted implicitly

### Validation

- pytest — 162 passed
- Ruff lint — passed
- Ruff format — 164 files already formatted
- mypy — 65 source files checked

---

## CORE-083 — Add Safe Local Synchronization

### Added

- Guarded `scripts/sync-titan.ps1` synchronization workflow
- VS Code tasks for safe synchronization and optional full validation

### Architectural Notes

- Updates require a clean local `main` and fast-forward-only history
- No automatic stashing, reset, branch switching, conflict resolution, or push

---

## CORE-082 — Validate Investigation Purpose

### Changed

- New investigations reject empty or whitespace-only purposes
- Valid purpose text remains unchanged
- Application validation failures use the existing Unit of Work rollback path
- Historical restoration behavior remains unchanged

### Validation

- pytest — 162 passed
- Ruff lint and format — passed
- mypy — 65 source files checked

---

## CORE-081 — Reconcile CORE-080 Continuity

### Changed

- Reconciled the CORE-080 specification and backlog after integration
- Restored accurate development continuity without changing production behavior

---

## CORE-080 — Close SQLite Test Resources

### Changed

- Closed bootstrap-created applications deterministically in tests
- Centralized tracked SQLite connection cleanup in test fixtures
- Removed resource-warning noise without changing application behavior

---

## CORE-079 — Protect Hypothesis Decisions on Closed Investigations

### Changed

- Closed investigations reject hypothesis confirmation and rejection
- Application use cases route hypothesis decisions through the aggregate
- Failed mutations preserve Unit of Work rollback behavior

---

## CORE-078 — Protect Evidence Addition on Closed Investigations

### Changed

- Closed investigations reject evidence addition
- Evidence mutation is routed through the investigation aggregate
- Failed application mutations preserve Unit of Work rollback behavior

---

## CORE-077 — Refresh Project Context

### Changed

- Refreshed the continuity reference through CORE-076
- Recorded current architecture, validation state, and GitHub workflow

---

## CORE-076 — Update README for Evidence Relationships

### Changed

- Documented explicit evidence relationship usage and persistence
- Updated the documented validation state through CORE-075

---

## CORE-075 — Classify Evidence Relationship

### Added

- `EvidenceRelationship` domain enum with `SUPPORTS`, `WEAKENS`, and `UNSPECIFIED`
- Explicit evidence relationship on `Evidence`
- Relationship support through the `AddEvidence` use case
- SQLite persistence and restoration of evidence relationships
- Automatic migration of legacy evidence schemas without a relationship column
- Acceptance coverage verifying relationship persistence across application reconstruction

### Changed

- New evidence must explicitly state whether it supports or weakens a hypothesis
- `AddEvidence` rejects `UNSPECIFIED` for newly recorded evidence
- Legacy persisted evidence is restored with `UNSPECIFIED` when no historical relationship exists

### Architectural Notes

- Evidence relationship is modeled in the domain
- `UNSPECIFIED` is reserved for historical compatibility
- `EvidenceAdded` remains unchanged
- Existing Unit of Work transaction behavior remains unchanged
- No evidence weighting introduced
- No confidence or certainty scoring introduced
- No assessment introduced
- No automatic hypothesis confirmation or rejection introduced
- No new runtime dependency introduced

### Validation

- Domain relationship modeling verified
- Application relationship propagation verified
- SQLite relationship persistence and restoration verified
- Legacy SQLite evidence schema migration verified
- Acceptance workflow preserves evidence relationship after application reconstruction
- pytest — 147 passed
- Ruff — passed
- mypy — 60 source files checked

---

## CORE-074 — Update README for Evidence Provenance

### Changed

- Updated the documented test suite size from 136 to 142 passing tests
- Updated the `add_evidence()` example to include the required evidence source
- Documented explicit application resource cleanup through `application.close()`
- Documented that persisted application reconstruction preserves evidence provenance

### Architectural Notes

- Documentation now reflects the evidence provenance behavior introduced in CORE-073
- Documentation now reflects application lifecycle management introduced in CORE-072
- No domain behavior changed
- No application behavior changed
- No SQLite persistence behavior changed
- No transaction behavior changed
- No new runtime dependency introduced

### Validation

- README usage matches the current `AddEvidence` signature
- README lifecycle usage matches `TitanApplication.close()`
- pytest — 142 passed
- Ruff — passed
- mypy — 60 source files checked

---

## CORE-073 — Record Evidence Source

### Added

- Required `source` field for `Evidence`
- Source validation in the domain model
- Evidence source support through the `AddEvidence` use case
- SQLite persistence and restoration of evidence source
- Automatic migration of legacy evidence schemas without a `source` column
- End-to-end acceptance coverage for evidence source persistence

### Changed

- `Evidence` now requires both a description and a source
- `AddEvidence` now requires a source when creating evidence
- The SQLite `evidences` table now stores `source TEXT NOT NULL`
- Legacy evidence rows without recorded provenance receive the explicit `legacy source unavailable` marker

### Architectural Notes

- Evidence provenance is modeled in the domain
- Application use cases pass provenance explicitly
- SQLite remains responsible for schema evolution
- Existing legacy evidence data is preserved during migration
- `EvidenceAdded` remains unchanged and continues to identify the hypothesis and evidence
- No source-type hierarchy introduced
- No external provenance service introduced
- No CLI introduced
- No HTTP API introduced
- No Event Bus introduced
- No Outbox introduced
- No AI provider integration introduced
- No new runtime dependency introduced

### Validation

- Domain evidence source validation verified
- Application evidence source propagation verified
- SQLite source persistence and restoration verified
- Legacy SQLite evidence schema migration verified
- Evidence source persistence across application reconstruction verified
- pytest — 142 passed
- Ruff — passed
- mypy — 60 source files checked

---

## CORE-072 — Add Application Lifecycle Management

### Added

- Explicit `close()` lifecycle operation for `SqliteUnitOfWork`
- Application-level `close()` operation on `TitanApplication`
- Infrastructure coverage verifying that SQLite connections are released
- Bootstrap coverage verifying application-level resource cleanup

### Architectural Notes

- SQLite connection ownership remains in the infrastructure layer
- `TitanApplication` delegates resource cleanup to the `SqliteUnitOfWork` created by the composition root
- Application use cases remain unaware of SQLite connection lifecycle details
- Existing commit and rollback transaction behavior remains unchanged
- Resource cleanup no longer relies solely on process shutdown or garbage collection
- No context manager support introduced
- No CLI lifecycle integration introduced
- No web framework lifecycle integration introduced
- No new runtime dependency introduced

### Validation

- `SqliteUnitOfWork.close()` releases the underlying SQLite connection
- Repository access after close raises `sqlite3.ProgrammingError`
- `TitanApplication.close()` releases application-owned SQLite resources
- pytest — 138 passed
- Ruff — passed
- mypy — 60 source files checked

---

## CORE-071 — Update Project README

### Changed

- Replaced the obsolete CORE-000 bootstrap status in the project README
- Documented the current TITAN Core capabilities
- Documented the domain, application, infrastructure, and composition boundaries
- Documented SQLite persistence and Unit of Work transaction coordination
- Documented `bootstrap(database)` and the `TitanApplication` API
- Added application usage examples for the persisted investigation workflow
- Documented the current testing strategy and architecture guards
- Documented the current project scope and explicitly excluded concerns

### Architectural Notes

- The documented application API was verified against `src/titan/bootstrap.py`
- The README reflects the existing architecture without introducing new production behavior
- TITAN Core remains independent from CLI, HTTP, web framework, Event Bus, Outbox, and AI provider concerns
- No production code changed
- No new runtime dependency introduced
- Repository-wide Ruff formatting cleanup remains outside this story

### Validation

- README saved without a UTF-8 BOM
- pytest — 136 passed
- Ruff — passed
- mypy — 60 source files checked

---

## CORE-070 — Add Application Acceptance Test

### Added

- End-to-end application acceptance coverage through `bootstrap()`
- Complete persisted investigation workflow using SQLite
- Application reconstruction verification against the same SQLite database

### Acceptance Coverage

- Create investigation
- Activate investigation
- Add hypothesis
- Add evidence
- Confirm hypothesis
- Close investigation
- Reconstruct the application
- Retrieve and verify the persisted aggregate
- List persisted investigations

### Architectural Notes

- The acceptance test interacts with TITAN through the application composition root
- Repositories and SQLite connections are not accessed directly by the acceptance scenario
- Persistence is verified across application reconstruction
- The scenario validates the complete path from application use cases through Unit of Work and SQLite
- No production code changed
- No new runtime dependency introduced

### Validation

- pytest — 136 passed
- Ruff — passed
- mypy — 60 source files checked

---

## CORE-069 — Introduce Application Composition Root

### Added

- `titan.bootstrap` application composition root
- `TitanApplication` composition object exposing all current application use cases
- `bootstrap(database)` factory for constructing a SQLite-backed application
- Integration coverage for application wiring through SQLite

### Architectural Notes

- Mutating use cases share a `SqliteUnitOfWork`
- Read-only investigation queries use the investigation repository exposed by the Unit of Work
- SQLite infrastructure knowledge remains outside the domain and application layers
- The composition root provides the outer wiring boundary for the application
- No CLI introduced
- No web framework introduced
- No Event Bus introduced
- No Outbox introduced
- No new runtime dependency introduced

### Validation

- Bootstrap persists and retrieves investigations through SQLite
- All current application use cases are exposed by the composition root
- pytest — 135 passed
- Ruff — passed
- mypy — 59 source files checked

---

## CORE-068 — Enforce Unit of Work for Mutating Use Cases

### Added

- Application-layer architecture guard for direct repository dependencies
- Explicit allowlist for intentional `InvestigationRepository` and `DomainEventRepository` dependencies
- Automatic protection for new application modules against prohibited direct repository dependencies

### Architectural Notes

- Mutating application use cases remain behind the `UnitOfWork` persistence boundary
- Read-only queries may continue to depend directly on `InvestigationRepository`
- Repository abstractions and in-memory implementations remain explicit exceptions
- `persist_domain_events()` may continue to depend directly on `DomainEventRepository`
- `UnitOfWork` may continue to reference both repository abstractions
- The architecture rule is enforced through Python AST inspection
- No production code changed
- No Event Bus introduced
- No Outbox introduced

### Validation

- Architecture guard passes on the current application layer
- A temporary prohibited repository dependency was correctly detected
- Removing the temporary violation restored the architecture test to green
- pytest — 133 passed
- Ruff — passed
- mypy — 57 source files checked

---

## CORE-067 — Migrate Reopen Investigation to Unit of Work

### Changed

- `ReopenInvestigation` now receives a `UnitOfWork`
- Investigation loading and persistence use `unit_of_work.investigations`
- `InvestigationReopened` event persistence uses `unit_of_work.domain_events`
- Successful persistence commits the Unit of Work
- Persistence failures roll back the Unit of Work
- Missing investigation behavior remains unchanged

### Architectural Notes

- `ReopenInvestigation` now defines an explicit transaction boundary
- Repository implementations remain behind the `UnitOfWork` abstraction
- `persist_domain_events()` remains the shared event persistence mechanism
- Pending domain events continue to be persisted from the `Investigation` aggregate
- No other application use case migrated
- No Event Bus introduced
- No Outbox introduced

### Validation

- pytest — 132 passed
- Ruff — passed
- mypy — 56 source files checked

---

## CORE-066 — Migrate Remove Hypothesis to Unit of Work

### Changed

- `RemoveHypothesis` now receives a `UnitOfWork`
- Investigation loading and persistence use `unit_of_work.investigations`
- `HypothesisRemoved` event persistence uses `unit_of_work.domain_events`
- Successful persistence commits the Unit of Work
- Persistence failures roll back the Unit of Work
- Missing investigation and hypothesis behavior remains unchanged

### Architectural Notes

- `RemoveHypothesis` now defines an explicit transaction boundary
- Repository implementations remain behind the `UnitOfWork` abstraction
- `persist_domain_events()` remains the shared event persistence mechanism
- Pending domain events continue to be persisted from the `Investigation` aggregate
- No other application use case migrated
- No Event Bus introduced
- No Outbox introduced

### Validation

- pytest — 130 passed
- Ruff — passed
- mypy — 56 source files checked

---

## CORE-065 — Migrate Close Investigation to Unit of Work

### Changed

- `CloseInvestigation` now receives a `UnitOfWork`
- Investigation loading and persistence use `unit_of_work.investigations`
- `InvestigationClosed` event persistence uses `unit_of_work.domain_events`
- Successful persistence commits the Unit of Work
- Persistence failures roll back the Unit of Work
- Missing investigation behavior remains unchanged

### Architectural Notes

- `CloseInvestigation` now defines an explicit transaction boundary
- Repository implementations remain behind the `UnitOfWork` abstraction
- `persist_domain_events()` remains the shared event persistence mechanism
- Pending domain events continue to be persisted from the `Investigation` aggregate
- No other application use case migrated
- No Event Bus introduced
- No Outbox introduced

### Validation

- pytest — 128 passed
- Ruff — passed
- mypy — 56 source files checked

---

## CORE-064 — Migrate Reject Hypothesis to Unit of Work

### Changed

- `RejectHypothesis` now receives a `UnitOfWork`
- Investigation loading and persistence use `unit_of_work.investigations`
- `HypothesisRejected` event persistence uses `unit_of_work.domain_events`
- Successful persistence commits the Unit of Work
- Persistence failures roll back the Unit of Work
- Missing investigation and hypothesis behavior remains unchanged

### Architectural Notes

- `RejectHypothesis` now defines an explicit transaction boundary
- Repository implementations remain behind the `UnitOfWork` abstraction
- `persist_domain_events()` remains the shared event persistence mechanism
- Pending domain events continue to be persisted from the `Hypothesis` entity
- No other application use case migrated
- No Event Bus introduced
- No Outbox introduced

### Validation

- pytest — 126 passed
- Ruff — passed
- mypy — 56 source files checked

---

## CORE-063 — Migrate Confirm Hypothesis to Unit of Work

### Changed

- `ConfirmHypothesis` now receives a `UnitOfWork`
- Investigation loading and persistence use `unit_of_work.investigations`
- `HypothesisConfirmed` event persistence uses `unit_of_work.domain_events`
- Successful persistence commits the Unit of Work
- Persistence failures roll back the Unit of Work
- Missing investigation and hypothesis behavior remains unchanged

### Architectural Notes

- `ConfirmHypothesis` now defines an explicit transaction boundary
- Repository implementations remain behind the `UnitOfWork` abstraction
- `persist_domain_events()` remains the shared event persistence mechanism
- Pending domain events continue to be persisted from the `Hypothesis` entity
- No other application use case migrated
- No Event Bus introduced
- No Outbox introduced

### Validation

- pytest — 124 passed
- Ruff — passed
- mypy — 56 source files checked

---

## CORE-062 — Migrate Activate Investigation to Unit of Work

### Changed

- `ActivateInvestigation` now receives a `UnitOfWork`
- Investigation loading and persistence use `unit_of_work.investigations`
- `InvestigationActivated` event persistence uses `unit_of_work.domain_events`
- Successful persistence commits the Unit of Work
- Persistence failures roll back the Unit of Work
- Missing investigation behavior remains unchanged

### Architectural Notes

- `ActivateInvestigation` now defines an explicit transaction boundary
- Repository implementations remain behind the `UnitOfWork` abstraction
- `persist_domain_events()` remains the shared event persistence mechanism
- No other application use case migrated
- No Event Bus introduced
- No Outbox introduced

### Validation

- pytest — 122 passed
- Ruff — passed
- mypy — 56 source files checked

---

## CORE-061 — Migrate Add Evidence to Unit of Work

### Changed

- `AddEvidence` now receives a `UnitOfWork`
- Investigation loading and persistence use `unit_of_work.investigations`
- `EvidenceAdded` event persistence uses `unit_of_work.domain_events`
- Successful persistence commits the Unit of Work
- Persistence failures roll back the Unit of Work
- Missing investigation and hypothesis behavior remains unchanged
- Evidence description validation remains unchanged

### Architectural Notes

- `AddEvidence` now defines an explicit transaction boundary
- Repository implementations remain behind the `UnitOfWork` abstraction
- `persist_domain_events()` remains the shared event persistence mechanism
- Pending domain events continue to be persisted from the `Hypothesis` entity
- No other application use case migrated
- No Event Bus introduced
- No Outbox introduced

### Validation

- pytest — 120 passed
- Ruff — passed
- mypy — 56 source files checked

---

## CORE-060 — Migrate Add Hypothesis to Unit of Work

### Changed

- `AddHypothesis` now receives a `UnitOfWork`
- Investigation loading and persistence use `unit_of_work.investigations`
- Domain event persistence uses `unit_of_work.domain_events`
- Successful persistence commits the Unit of Work
- Persistence failures roll back the Unit of Work
- Missing investigations continue to raise `LookupError`

### Architectural Notes

- `AddHypothesis` now defines an explicit transaction boundary
- Repository implementations remain behind the `UnitOfWork` abstraction
- `persist_domain_events()` remains the shared event persistence mechanism
- No other application use case migrated
- No Event Bus introduced
- No Outbox introduced

### Validation

- pytest — 118 passed
- Ruff — passed
- mypy — 56 source files checked

---

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
