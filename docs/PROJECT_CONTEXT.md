# TITAN Core — Project Context

## Purpose

This document is the continuity and recovery reference for TITAN Core.

Its purpose is to preserve the architectural intent, product vision,
development method, current implementation state, and direction of the project
independently of any individual development session or conversation.

When development resumes in a new environment or conversation, review this
document together with:

- `docs/BACKLOG.md`;
- `docs/CHANGELOG.md`;
- the latest specifications under `docs/specs/`;
- current source code and tests;
- current GitHub pull requests and CI state;
- relevant Git history when necessary.

This document distinguishes between:

- functionality that exists today;
- accepted architectural principles;
- long-term product vision;
- ideas that remain exploratory.

Future vision must not be mistaken for implemented behavior or an accepted
backlog requirement.

---

## Foundational Vision

TITAN is being built to improve human judgment under uncertainty.

Its purpose is not simply to produce predictions, recommendations, or
AI-generated answers.

The long-term goal is to help a person conduct structured research, understand
the evidence behind a conclusion, expose uncertainty and competing
explanations, maintain reasoning over time, and ultimately make a better human
decision.

A useful conceptual direction is:

```text
Question
    ↓
Investigation
    ↓
Evidence
    ↓
Claims
    ↓
Interpretations
    ↓
Hypotheses
    ↓
Thesis
    ↓
Assessment
    ↓
Human Decision
```

Not every concept in this chain exists in the current implementation. It
represents the broader reasoning model TITAN may progressively develop.

A conventional AI system may attempt to transform a question directly into an
answer. TITAN should instead preserve the reasoning structure between the
question and the eventual decision.

The human remains responsible for final judgment.

---

## Finance as the First Domain

TITAN is currently being developed through investment research.

Finance is the first practical domain in which the reasoning architecture is
being exercised, but the deepest architectural concepts should remain as
domain-neutral as practical.

The Core should prefer concepts such as:

- Investigation;
- Hypothesis;
- Evidence;
- Assessment;
- Report;
- Event;
- Workflow.

Financial concepts such as stocks, options, valuation models, tickers, entry
prices, or trading strategies should not leak into the reasoning kernel unless
there is a demonstrated architectural reason.

A useful architectural test is:

> If a Core concept can only be justified using stock-market vocabulary, it
> probably belongs in a finance-specific layer rather than the reasoning Core.

---

## Product and Reasoning Vision

TITAN should eventually help users understand:

- what something means;
- why a factor matters;
- what evidence supports an idea;
- what evidence weakens an idea;
- where evidence came from;
- what could invalidate a thesis;
- how reasoning changed over time;
- how to reason about uncertainty.

An experienced user should eventually be able to inspect deeper structures such
as:

- hypotheses;
- supporting and weakening evidence;
- provenance;
- uncertainty;
- contradictions;
- historical changes;
- assessments;
- invalidation conditions.

The desired direction is one reasoning engine with different levels of
presentation and interaction rather than separate systems for different user
levels.

Natural-language and voice interaction remain long-term interface directions.
Reasoning must remain independent from its presentation mechanism.

---

## Living Research

A central long-term idea is that a thesis should not be treated as a static
document produced once and forgotten.

TITAN should eventually support research that evolves as reality changes.

New evidence may:

- strengthen a hypothesis;
- weaken a hypothesis;
- contradict previous information;
- create a new question;
- change an assessment;
- invalidate part of a thesis;
- justify reopening an investigation.

Historical traceability matters because TITAN should eventually be able to
explain not only what is believed now, but what changed and why.

The current persistence and domain-event capabilities are foundational pieces
toward this objective. TITAN Core does not currently implement full event
sourcing.

---

## Human Judgment

TITAN should augment human judgment rather than replace it.

Future automation may collect information, structure evidence, execute
specialized analytical capabilities, identify contradictions, compare
hypotheses, generate reports, and explain reasoning.

The final investment decision remains a human responsibility.

A successful TITAN should help its user become a better reasoner rather than
merely become dependent on automated answers.

---

## AI and Cognitive Capabilities

TITAN should not be architecturally dependent on a particular AI model or
provider.

Future cognitive capabilities may be implemented by remote language models,
local models, deterministic algorithms, rules, specialized analytical systems,
humans, or combinations of these.

The Core should depend on meaningful contracts and structured results rather
than on the identity of the provider that produced them.

AI should not be allowed to arbitrarily mutate authoritative domain state.

AI integration remains future architecture and must be introduced incrementally
when a concrete requirement justifies it.

---

## Future Reasoning Concepts

Historical design work explored concepts that may become important as TITAN
evolves, including:

- Thesis;
- Claim;
- Interpretation;
- Assessment;
- Expert Report;
- Contradiction;
- Open Question;
- richer evidence relationships;
- knowledge evolution.

These concepts are preserved as direction, not automatically accepted
requirements.

Before introducing a future concept into the implementation:

1. establish the concrete domain need;
2. define the concept precisely;
3. write a focused CORE story;
4. create a specification;
5. introduce behavior using TDD when production behavior changes.

Abstractions must be earned by demonstrated requirements rather than added
because they appeared in historical design discussions.

---

## Current Implemented Core

The primary aggregate is `Investigation`.

An investigation currently contains:

- `InvestigationId`;
- title;
- purpose;
- investigation status;
- hypotheses;
- provisional theses;
- closure timestamp when applicable.

### Investigation lifecycle

Current statuses are:

- `DRAFT`;
- `ACTIVE`;
- `CLOSED`.

Supported lifecycle operations include create, activate, close, and reopen.
Closed investigations prevent modifications until reopened.

### Hypotheses

Investigations contain hypotheses with their own identity and status.

Current hypothesis behavior includes:

- adding hypotheses;
- preventing duplicate hypotheses;
- finding hypotheses;
- removing hypotheses;
- confirming hypotheses;
- rejecting hypotheses.

Hypothesis statuses are `PENDING`, `CONFIRMED`, and `REJECTED`.

### Evidence

Evidence belongs to a hypothesis and currently records:

- `EvidenceId`;
- description;
- source provenance;
- relationship to the hypothesis.

`EvidenceRelationship` currently supports:

- `SUPPORTS`;
- `WEAKENS`;
- `UNSPECIFIED`.

New evidence created through the application layer must explicitly use either
`SUPPORTS` or `WEAKENS`.

`UNSPECIFIED` is reserved for persisted legacy evidence whose historical
relationship was not recorded.

Evidence source and relationship are persisted through SQLite and survive
application reconstruction.

Current evidence behavior does not include weighting, numeric scoring,
confidence, certainty, assessment, automatic hypothesis decisions, claims, or
interpretations.

---

## Domain Events

TITAN uses domain events to represent meaningful facts that occurred inside the
domain.

Current domain events include:

- `InvestigationCreated`;
- `InvestigationActivated`;
- `InvestigationClosed`;
- `InvestigationReopened`;
- `HypothesisAdded`;
- `HypothesisRemoved`;
- `HypothesisConfirmed`;
- `HypothesisRejected`;
- `EvidenceAdded`.

Domain entities record events internally and expose pending events through
`pull_events()`.

The domain model does not depend on event persistence infrastructure.

`EvidenceAdded` identifies the hypothesis and evidence. Evidence provenance and
relationship remain aggregate state and are not duplicated into that event.

---

## Application Layer

The application layer orchestrates domain behavior through use cases and
persistence abstractions.

Current application operations include:

- creating investigations;
- activating investigations;
- closing investigations;
- reopening investigations;
- retrieving investigations;
- listing investigations;
- adding hypotheses;
- removing hypotheses;
- confirming hypotheses;
- rejecting hypotheses;
- adding evidence;
- adding claims;
- adding interpretations;
- adding provisional theses.

Mutating use cases operate through `UnitOfWork`.

A mutation coordinates investigation persistence and domain-event persistence
within one transaction boundary. Successful operations commit; failures roll
back.

Read-only investigation queries depend on repository abstractions.

---

## Persistence

### Investigation persistence

`InvestigationRepository` defines the application-level persistence contract.
Current implementations include:

- `InMemoryInvestigationRepository`;
- `SqliteInvestigationRepository`.

SQLite persistence restores:

- investigation identity and lifecycle state;
- closure timestamp;
- hypotheses and hypothesis status;
- evidence identity and description;
- evidence source;
- evidence relationship;
- provisional thesis identity, statement, ownership, and insertion order.

SQLite automatically migrates legacy evidence schemas that lack source or
relationship columns. Historical rows without recorded provenance receive the
explicit legacy source marker, and rows without historical relationship data
restore as `UNSPECIFIED`.

### Domain event persistence

`DomainEventRepository` defines the domain-event persistence contract. Current
implementations include:

- `InMemoryDomainEventRepository`;
- `SqliteDomainEventRepository`.

SQLite provides durable ordered event persistence for the current supported
domain-event set.

### Unit of Work

`UnitOfWork` is the transaction boundary used by mutating application use cases.
`SqliteUnitOfWork` coordinates investigation and domain-event repositories over
a shared SQLite connection.

---

## Composition and Lifecycle

`src/titan/bootstrap.py` is the composition root.

`bootstrap(database)` constructs a SQLite-backed `TitanApplication` exposing the
current application use cases.

`TitanApplication.close()` explicitly releases application-owned SQLite
resources through the Unit of Work lifecycle.

Application and domain code remain unaware of SQLite connection details.

---

## Architecture Principles

### Dependency Direction

Dependencies point inward. The Core domain remains independent from SQLite,
interfaces, AI providers, and other infrastructure technologies.

### Domain Neutrality

The reasoning Core avoids unnecessary dependence on a particular investment
instrument, strategy, interface, or AI provider.

### Repository and Transaction Boundaries

Application code depends on abstractions. Concrete persistence and SQLite
transaction management belong in infrastructure.

### Explicit Reasoning

Important conclusions should eventually be explainable through explicit
research structures rather than hidden inside opaque outputs.

### Historical Integrity

Changes to knowledge should remain traceable where the domain requires it. New
functionality should not destroy historical information without an explicit
reason.

### Human Authority

TITAN assists human reasoning and does not remove human responsibility for
investment decisions.

### Test-Driven Development

Production behavior is normally developed using:

1. RED — introduce a failing test describing the required behavior;
2. GREEN — implement the minimum behavior necessary to satisfy the test;
3. REFACTOR — improve the implementation while keeping the suite green.

Documentation-only stories do not require artificial failing tests, but they
must still preserve the existing quality gates.

### Small Stories

Development proceeds through numbered CORE stories. Each story has a focused
responsibility and should not silently expand into unrelated architectural
work.

### Earned Abstractions

Abstractions are earned, not invented.

---

## Quality Gates

Before a CORE story is considered complete, the repository CI must pass the
current primary quality gates:

```text
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest
```

The GitHub Actions workflow executes these gates for pull requests.

---

## Development Method

The normal development sequence is:

```text
Specification
    ↓
RED when behavior changes
    ↓
GREEN
    ↓
REFACTOR
    ↓
Review
    ↓
Full Validation
    ↓
Pull Request
    ↓
CI
    ↓
Integration
```

Before adding a new production capability:

1. identify the concrete need;
2. inspect the existing implementation;
3. define the smallest story;
4. write its specification;
5. create a failing test;
6. implement the minimum behavior;
7. refactor only when justified;
8. run the complete quality gates.

A recurring question is:

> Are we increasing TITAN's ability to reason, or merely increasing the amount
> of code?

---

## Git and GitHub Workflow

The preferred workflow is now:

1. Start from current `main`.
2. Create `feature/CORE-XXX` from `main`.
3. Create or update the story specification.
4. Develop the focused change.
5. Keep continuity documentation current when the story materially changes
   project state.
6. Open a pull request targeting `main`.
7. Let GitHub Actions execute the quality gates.
8. Review the final diff and CI result.
9. Integrate only after CI succeeds.
10. Verify `main` points to the integrated story.

GitHub is the durable technical source of truth. A local VS Code checkout may
be synchronized from `main`, but local editor state is not the canonical
project state.

Avoid unrelated changes in story branches and pull requests.

---

## Source of Truth

### What exists today?

Prefer, in order:

1. current source code;
2. current tests;
3. latest completed specifications;
4. current backlog and changelog;
5. current GitHub `main` and CI state;
6. this document for summarized continuity.

If this document disagrees with implementation or tests, inspect the live
repository before proceeding and update this document through a focused story.

### Why does TITAN exist and where is it intended to go?

Use this document together with accepted architectural decision records and
preserved historical design material.

Historical discussions are valuable for recovering intent, but an idea from a
historical conversation is not automatically an accepted current requirement.

---

## Current Development State

State after CORE-131 implementation:

- last completed story: `CORE-131 — Cover Thesis Workflow Acceptance`;
- latest integrated baseline before CORE-131: `8156616 — CORE-130: add thesis use case`;
- GitHub's configured default branch is `main`;
- current validated suite: 288 passing tests;
- Ruff lint: passing;
- Ruff format: passing;
- mypy: passing;
- application composition, SQLite persistence, Unit of Work transaction
  coordination, application lifecycle management, evidence provenance,
  evidence relationship classification, closed-investigation aggregate
  protections, non-empty investigation purpose validation, repeated hypothesis
  decision protection, decided-hypothesis removal and evidence protection,
  orphaned SQLite evidence cleanup, investigation closure-schema migration,
  minimal event-store migration, and evidence identity protection are
  implemented; unknown persisted event types and incomplete event payloads are
  rejected explicitly, and malformed UUID and datetime payloads include event
  and field context; cross-hypothesis evidence identity ownership and
  whitespace-normalized hypothesis uniqueness are enforced; malformed
  persisted investigation identifiers, statuses, and closure timestamps are
  reported with record and field context; malformed persisted hypothesis
  identifiers and statuses receive equivalent contextual diagnostics;
  malformed persisted evidence identifiers and relationships also receive
  contextual diagnostics; malformed persisted claim identifiers and evidence
  references receive equivalent contextual diagnostics; malformed persisted
  interpretation identifiers and claim references also receive contextual
  diagnostics; blank required
  persisted text is rejected across investigation, hypothesis, evidence,
  claim, and interpretation records; persisted claims whose evidence reference
  is not owned by their hypothesis are rejected with claim context; persisted
  interpretations whose claim reference is not owned by their hypothesis are
  rejected with interpretation context; restored investigations enforce
  whitespace-normalized hypothesis statement uniqueness;
  restored investigations also enforce exclusive evidence identity ownership;
  an immutable evidence-grounded `Claim` model with explicit identity is
  available as the first richer reasoning structure; claim identities cannot
  be reused across hypotheses during aggregate mutation or restoration; pending hypotheses own
  claims grounded in evidence already in their collection and emit
  `ClaimAdded` when attachment succeeds; claim attachment routes through the
  owning investigation for lifecycle and hypothesis lookup protection; claims
  are saved and reconstructed by the SQLite investigation repository;
  `ClaimAdded` is serialized with hypothesis, claim, and evidence identities;
  `AddClaim` coordinates both persistence paths through Unit of Work and is
  exposed by `bootstrap()`; the composed acceptance workflow verifies thesis
  reconstruction after a real SQLite-backed application restart; the composed acceptance workflow verifies claim
  reconstruction after a real SQLite-backed application restart;
  an immutable `Interpretation` model connects one claim to one hypothesis with
  an explicit rationale; pending hypotheses own interpretations and validate
  both hypothesis and claim references before emitting `InterpretationAdded`;
  interpretation attachment routes through the owning investigation lifecycle;
  interpretations are saved and reconstructed by the SQLite investigation
  repository after their claims;
  `InterpretationAdded` is serialized with hypothesis, interpretation, and
  claim identities by the SQLite event repository; `AddInterpretation`
  coordinates aggregate and event persistence through Unit of Work and is
  exposed by `bootstrap()`; the composed acceptance workflow verifies
  interpretation reconstruction after a real SQLite-backed application restart;
  interpretation identities cannot be reused across hypotheses during aggregate
  mutation or restoration; an immutable provisional `Thesis` model with
  explicit identity and non-blank statement is available; open investigations
  own theses, expose them as an immutable tuple, emit `ThesisAdded`, and reject
  duplicate thesis identities or attachment while closed; SQLite saves and
  reconstructs those theses without replaying mutation events; the SQLite event
  store persists `ThesisAdded` with investigation and thesis identities;
  `AddThesis` coordinates both persistence paths through Unit of Work and is
  exposed by `bootstrap()`;
- guarded PowerShell synchronization and VS Code tasks are available for a
  clean local `main` checkout;
- no confidence scoring, assessment, thesis selection or synthesis, Event Bus,
  Outbox, CLI,
  HTTP API, or AI provider integration is implemented.

CORE-131 proves the complete composed thesis workflow across a real
SQLite-backed application restart without introducing new production behavior.

---

## Long-Term Direction

The long-term direction is a progression rather than a fixed implementation
roadmap:

```text
Current Foundation
    ↓
Investigation Lifecycle
    ↓
Hypotheses
    ↓
Evidence
    ↓
Historical Traceability
    ↓
Evidence Provenance
    ↓
Evidence Relationships
    ↓
Richer Reasoning Structures
    ↓
Claims / Interpretations
    ↓
Thesis
    ↓
Reports / Capabilities
    ↓
Assessment
    ↓
Living Research
    ↓
Adaptive User Experience
    ↓
Conversational / Voice Interfaces
```

The exact order must be determined incrementally. The existence of this vision
must not be used to justify premature implementation.

---

## Next Development Step

After CORE-131 is complete, do not infer CORE-132 solely from the conceptual
roadmap.

Before defining the next story:

1. verify `main` and CI state;
2. review `BACKLOG.md`, `CHANGELOG.md`, and recent specifications;
3. inspect the current domain, application, persistence, and acceptance tests;
4. identify the smallest demonstrated reasoning capability that should come
   next;
5. define CORE-132 explicitly;
6. write its specification before production implementation.

Potential future reasoning concepts remain candidates until a concrete domain
need is established.

---

## Continuity Instructions

When resuming TITAN Core development in a new conversation or development
session:

1. inspect GitHub `main` and the latest merged pull request;
2. read this document;
3. read the bottom of `docs/BACKLOG.md` for the active or last completed story;
4. read the latest entry in `docs/CHANGELOG.md` and the latest specifications;
5. inspect relevant source code and tests before making architectural
   assumptions;
6. verify whether a feature branch or pull request is already active;
7. continue existing work rather than recreating completed functionality.

Always distinguish:

1. what is implemented;
2. what has been formally accepted;
3. what is long-term vision;
4. what was merely explored historically.

GitHub repository state is the durable recovery mechanism. Conversation memory
is helpful context, but it is not the sole source of project continuity.
