# TITAN Core — Project Context

## Purpose

This document is the continuity and recovery reference for TITAN Core.

Its purpose is to preserve the architectural intent, product vision,
development methodology, current state, and direction of the project
independently of any individual development session or conversation.

When development resumes in a new environment or conversation, this document
should be reviewed together with:

- `docs/BACKLOG.md`
- `docs/CHANGELOG.md`
- the specifications under `docs/specs/`
- current source code and tests
- relevant Git history

This document intentionally distinguishes between:

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

Not every concept in this chain exists in the current implementation.

It represents the broader reasoning model TITAN may progressively develop.

The distinction is fundamental:

A conventional AI system may attempt to transform a question directly into an
answer.

TITAN should instead preserve the reasoning structure between the question and
the eventual decision.

The human remains responsible for the final judgment.

---

## Finance as the First Domain

TITAN is currently being developed through investment research.

Finance is the first practical domain in which the reasoning architecture is
being exercised, but the deepest architectural concepts should remain as
domain-neutral as practical.

The Core should prefer concepts such as:

- Investigation
- Hypothesis
- Evidence
- Assessment
- Report
- Event
- Workflow

over concepts that only make sense for a specific financial instrument or
strategy.

Financial concepts such as stocks, options, valuation models, tickers, entry
prices, or trading strategies should not leak into the reasoning kernel unless
there is a demonstrated architectural reason.

A useful architectural test is:

If a Core concept can only be justified using stock-market vocabulary, it
probably belongs in a finance-specific layer rather than the reasoning Core.

---

## Product Vision

The long-term product should be useful to people with very different levels
of investment experience.

A beginner should be able to ask TITAN to explain:

- what something means;
- why a factor matters;
- what evidence supports an idea;
- what could invalidate an investment thesis;
- how to reason about uncertainty.

An experienced investor should be able to inspect deeper structures such as:

- hypotheses;
- supporting and weakening evidence;
- provenance;
- uncertainty;
- contradictions;
- historical changes;
- assessments;
- invalidation conditions.

The intention is not to build two unrelated systems.

The desired direction is one reasoning engine with different levels of
presentation and interaction.

Names such as "beginner mode" or "expert mode" should not be considered
accepted product requirements until formally specified.

The underlying principle is adaptive depth:

TITAN should be accessible without becoming superficial and powerful without
forcing every user to confront all of its internal complexity.

---

## Investment Scope

TITAN should not be conceptually restricted to a single investment style.

The broader product vision includes the possibility of supporting research
across different approaches such as:

- long-term investing;
- growth investing;
- value-oriented research;
- trading;
- portfolio analysis;
- comparative research;
- event-driven research;
- options and other investment instruments.

These capabilities are future product directions, not current TITAN Core
functionality.

The reasoning engine should remain sufficiently general that different
investment styles can use the same underlying research architecture while
placing different emphasis on evidence, capabilities, and assessments.

---

## Living Investment Research

A central long-term idea is that an investment thesis should not be treated as
a static document produced once and forgotten.

TITAN should eventually support research that evolves as reality changes.

New evidence may:

- strengthen a hypothesis;
- weaken a hypothesis;
- contradict previous information;
- create a new question;
- change an assessment;
- invalidate part of a thesis;
- justify reopening an investigation.

This makes historical traceability important.

TITAN should be capable of explaining not only:

"What do we currently believe?"

but eventually also:

"What did we believe before?"

"What changed?"

"What evidence caused the change?"

"Why did the assessment change?"

The persistence and domain-event capabilities being built today are
foundational pieces toward this longer-term objective.

---

## Human Judgment

TITAN should augment human judgment rather than replace it.

The system may eventually collect information, structure evidence, execute
specialized analytical capabilities, identify contradictions, compare
hypotheses, generate reports, and explain reasoning.

The final investment decision remains a human responsibility.

TITAN should help the user understand why a conclusion exists rather than
merely presenting a recommendation.

A successful TITAN should make its user a better reasoner over time, not merely
make the user dependent on automated answers.

---

## Conversational and Voice Experience

Natural-language interaction is part of the long-term product vision.

A future user should be able to ask questions such as:

- Why are we waiting?
- What evidence matters most?
- What would have to happen for the thesis to change?
- What could invalidate this hypothesis?
- Compare this investigation with another one.
- Explain this to me as a beginner.
- Show me the deeper evidence behind that conclusion.

Voice may eventually become another interface to the same reasoning system.

Possible experiences explored historically include:

- text-only interaction;
- an assistant that speaks when something important changes;
- a more proactive mentor-like experience.

Voice is not part of the current Core and should not contain independent
investment reasoning.

The desired architectural direction is:

Reasoning
    ↓
Structured Knowledge
    ↓
Explanation
    ↓
Text / Voice / Other Interfaces

The intelligence should exist independently of its presentation mechanism.

---

## AI and Cognitive Capabilities

TITAN should not be architecturally dependent on a particular AI model or
provider.

Future cognitive capabilities may be implemented by:

- remote language models;
- local models;
- deterministic algorithms;
- rules;
- specialized analytical systems;
- humans;
- combinations of these.

The Core should depend on meaningful contracts and structured results rather
than on the identity of the provider that produced them.

AI should not be allowed to arbitrarily mutate authoritative domain state.

A future architecture may use capabilities or expert workflows to produce
reports, proposals, evidence, or assessments that are subsequently integrated
through controlled application and domain behavior.

This remains future architecture and must be introduced incrementally when
real requirements justify it.

---

## Historical Traceability

Historical reconstruction is an important architectural direction.

TITAN should avoid silently destroying the reasoning history that explains how
an investigation reached its current state.

Domain events are one mechanism that can contribute to this capability.

The long-term objective is not merely persistence of current state.

It is the ability to understand the evolution of knowledge and reasoning over
time.

This does not mean TITAN Core currently implements full event sourcing.

No such assumption should be made unless explicitly introduced by a future
story and specification.

---

## Future Reasoning Concepts

Historical design work explored several concepts that may become important as
TITAN evolves.

These include:

- Thesis
- Claim
- Interpretation
- Provenance
- Assessment
- Expert Report
- Contradiction
- Open Question
- Evidence relationships
- Knowledge evolution

These concepts are preserved here because they form part of TITAN's broader
reasoning vision.

They are not automatically accepted requirements.

Before introducing any of them into the implementation:

1. establish the concrete domain need;
2. define the concept precisely;
3. write a focused CORE story;
4. create a specification;
5. introduce the behavior using TDD.

Abstractions must be earned by demonstrated requirements rather than added
because they appeared in historical design discussions.

---

## Current Implemented Core

The sections below describe functionality that actually exists in the current
TITAN Core implementation.

The primary aggregate is `Investigation`.

An investigation currently contains:

- `InvestigationId`
- title
- purpose
- investigation status
- hypotheses
- closure timestamp when applicable

An investigation controls its own lifecycle and protects its domain
invariants.

### Investigation lifecycle

Current statuses:

- `DRAFT`
- `ACTIVE`
- `CLOSED`

Supported lifecycle operations include:

- create
- activate
- close
- reopen

Closed investigations prevent modifications until reopened.

---

## Hypotheses

Investigations contain hypotheses.

A hypothesis has its own identity and lifecycle.

The domain currently supports:

- adding hypotheses;
- preventing duplicate hypotheses;
- finding hypotheses;
- removing hypotheses;
- confirming hypotheses;
- rejecting hypotheses.

Hypotheses may contain evidence used during the research process.

---

## Evidence

Evidence currently belongs to hypotheses.

Evidence has its own identity and description and is persisted together with
the investigation aggregate.

The current Evidence model is intentionally small.

Richer concepts such as provenance, reliability, source information, and
supporting or weakening relationships remain possible future domain
capabilities and should not be assumed to exist today.

---

## Domain Events

TITAN uses domain events to represent meaningful facts that occurred inside
the domain.

Current investigation domain events include:

- `InvestigationCreated`
- `InvestigationActivated`
- `InvestigationClosed`
- `InvestigationReopened`
- `HypothesisAdded`
- `HypothesisRemoved`

Domain entities record events internally and expose them through
`pull_events()`.

The domain model does not depend on event persistence infrastructure.

Domain events should remain meaningful domain facts rather than infrastructure
messages.

---

## Application Layer

The application layer orchestrates domain behavior through use cases and
repository abstractions.

Implemented use cases include operations for:

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
- adding evidence.

Application code depends on abstractions rather than concrete persistence
implementations.

---

## Persistence

### Investigation persistence

`InvestigationRepository` defines the application-level persistence
abstraction.

Implementations currently include:

- `InMemoryInvestigationRepository`
- `SqliteInvestigationRepository`

SQLite persistence restores:

- investigation identity;
- title;
- purpose;
- status;
- closure timestamp;
- hypotheses;
- hypothesis status;
- evidence.

### Domain event persistence

`DomainEventRepository` defines the abstraction for storing domain events.

Implementations currently include:

- `InMemoryDomainEventRepository`
- `SqliteDomainEventRepository`

The SQLite implementation provides durable, ordered domain event persistence.

It currently supports persistence and restoration of:

- `InvestigationCreated`
- `InvestigationActivated`
- `InvestigationClosed`
- `InvestigationReopened`
- `HypothesisAdded`
- `HypothesisRemoved`

Event-specific data such as closure timestamps, hypothesis statements, and
hypothesis identifiers is preserved.

The existence of durable domain-event persistence does not by itself imply
that all application use cases automatically persist or publish generated
events.

That integration must be introduced explicitly through future stories.

---

## Architecture Principles

TITAN Core follows these principles.

### Domain-Driven Design

Business rules belong in the domain model.

Infrastructure must not leak into the domain.

### Dependency Direction

Dependencies should point inward.

The Core domain must remain independent from SQLite, user interfaces, AI
providers, and other infrastructure technologies.

### Domain Neutrality

The reasoning Core should avoid unnecessary dependence on a particular
investment instrument, strategy, interface, or AI provider.

### Repository Abstractions

Application code works against repository abstractions.

Concrete persistence belongs in infrastructure.

### Explicit Reasoning

Important conclusions should eventually be explainable through explicit
research structures rather than hidden inside opaque outputs.

### Historical Integrity

Changes to knowledge should eventually be traceable.

New functionality should avoid destroying historical information without an
explicit domain reason.

### Human Authority

TITAN assists human reasoning.

It does not remove human responsibility for investment decisions.

### Test-Driven Development

New behavior is normally developed using:

1. RED — introduce a failing test describing the required behavior.
2. GREEN — implement the minimum behavior necessary to satisfy the test.
3. REFACTOR — improve the implementation while keeping the suite green.

Existing behavior must remain protected by the full test suite.

### Small Stories

Development proceeds through numbered CORE stories.

Each story should have a focused responsibility and should not silently expand
into unrelated architectural work.

Large future concepts should be decomposed into the smallest useful behavior
that can be specified and tested.

### Earned Abstractions

Do not introduce an abstraction merely because it may become useful later.

A recurring design principle is:

Abstractions are earned, not invented.

### Quality Gates

Before a CORE story is considered complete, run:

`uv run pytest`

`uv run ruff check .`

`uv run mypy src`

All three must pass.

---

## Development Method

The normal development sequence is:

Specification
    ↓
RED
    ↓
GREEN
    ↓
REFACTOR
    ↓
Review
    ↓
Full Validation
    ↓
Commit
    ↓
Integration

Do not skip directly from an architectural idea to a large implementation.

Before adding a new capability:

1. identify the concrete need;
2. inspect the existing implementation;
3. define the smallest story;
4. write or update its specification;
5. create a failing test;
6. implement the minimum behavior;
7. refactor only when justified;
8. run the complete quality gates.

A useful recurring question is:

"Are we increasing TITAN's ability to reason, or merely increasing the amount
of code?"

---

## Git Workflow

Development normally follows this workflow:

1. Start from an up-to-date `main`.
2. Create `feature/CORE-XXX`.
3. Develop using TDD.
4. Run the complete quality gates.
5. Update the specification, backlog, and changelog as appropriate.
6. Review `git status`.
7. Commit only the files belonging to the story.
8. Push the feature branch.
9. Switch to `main`.
10. Integrate using `git merge --ff-only feature/CORE-XXX`.
11. Push `main`.

Avoid unrelated changes in story commits.

---

## Source of Truth

Different sources answer different questions.

### What exists today?

Prefer:

1. current source code;
2. current tests;
3. current specifications;
4. current backlog and changelog;
5. Git history.

### Why does TITAN exist and where is it intended to go?

Use:

1. this document;
2. accepted architectural decision records when available;
3. preserved historical design material.

Historical discussions are valuable for recovering intent, but an idea from a
historical conversation is not automatically an accepted current requirement.

If documentation and implementation disagree about current behavior, inspect
the implementation and tests before proceeding.

---

## Current Development State

Last completed story:

`CORE-042 — Add SQLite Domain Event Repository`

Last integrated story commit:

`3d0cf9e — CORE-042: add SQLite domain event repository`

Current branch after integration:

`main`

Validation at completion of CORE-042:

- pytest: 95 passed
- Ruff: passed
- mypy: passed on 26 source files

CORE-042 is integrated into `main` and pushed to `origin/main`.

---

## Next Development Step

`CORE-043` has not yet been defined.

Do not assume its requirements solely from its number or from historical
roadmaps.

Before implementation:

1. review the current architecture;
2. review `BACKLOG.md` and recent specifications;
3. review relevant recovered architectural decisions;
4. inspect the current application and persistence boundaries;
5. identify the next smallest architectural capability required by TITAN;
6. define CORE-043 explicitly;
7. write its specification;
8. begin implementation using TDD.

One demonstrated architectural question currently exists:

Domain aggregates generate domain events and TITAN now has durable domain-event
persistence, but application use cases do not yet necessarily coordinate
aggregate persistence with domain-event persistence.

The correct solution has not yet been accepted.

Possible approaches must be evaluated from the current architecture rather
than assumed from historical discussions.

Reliable event publication, transaction coordination, dispatch, or other
patterns may become relevant, but none should be introduced until the concrete
requirement is established.

---

## Long-Term Direction

The long-term direction should be understood as a progression rather than a
fixed implementation roadmap.

A possible conceptual evolution is:

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
Richer Evidence Relationships
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

The exact order must be determined incrementally.

The existence of this vision must not be used to justify premature
implementation.

---

## Continuity Instructions

When resuming TITAN Core development in a new conversation or development
session, begin by establishing the current repository state.

Review:

- this document;
- the backlog;
- the changelog;
- the latest specifications;
- relevant source code;
- relevant tests;
- Git history when necessary.

Then distinguish:

1. what is implemented;
2. what has been formally accepted;
3. what is long-term vision;
4. what was merely explored historically.

Do not recreate completed functionality.

Do not assume that an idea discussed previously became an accepted
requirement unless it is represented in the repository or explicitly
confirmed.

Do not allow enthusiasm for the long-term vision to bypass incremental
development discipline.

Continue from the last completed CORE story using the same small-story,
test-driven development process.

---

## North Star

TITAN should not become a machine that merely produces more answers.

It should become a system that helps humans investigate better, preserve the
reasoning behind their beliefs, recognize when evidence changes those beliefs,
understand uncertainty, and make better decisions.

Technology will change.

AI providers will change.

Interfaces will change.

Investment instruments and analytical techniques will change.

The reasoning model, historical traceability, and commitment to improving
human judgment are the architectural assets TITAN Core should protect.
