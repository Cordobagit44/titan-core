# TITAN Core

> Evidence. Reasoning. Confidence.

TITAN Core is the domain foundation of a platform for traceable investigations.
It preserves the reasoning chain from evidence to assessment while keeping the
domain independent from databases, APIs, user interfaces, and AI vendors.

## Status

TITAN Core currently provides a tested domain and application foundation for
investigation workflows.

Implemented capabilities include:

- investigation creation, activation, closing, and reopening;
- validation that new investigations include a non-empty purpose;
- hypothesis creation, pending-hypothesis removal, confirmation, and rejection;
- evidence attached to pending hypotheses with explicit provenance and relationship classification;
- SQLite-persisted evidence-grounded claims owned by pending hypotheses;
- SQLite-persisted immutable interpretations owned by pending hypotheses with validated claim links;
- investigation-owned provisional theses with SQLite state and domain-event persistence;
- investigation-owned narrative assessments linked to theses, without verdicts or numeric confidence;
- domain event emission and persistence;
- SQLite persistence for investigations and domain events;
- transaction coordination through Unit of Work;
- application composition through `bootstrap()`;
- architecture guards for domain and application dependencies;
- end-to-end acceptance coverage through the composed application.

The current test suite contains 321 passing tests.

## Architecture

TITAN Core follows a layered architecture with explicit dependency boundaries.

```text
                  +----------------------+
                  |   Composition Root   |
                  |   titan.bootstrap    |
                  +----------+-----------+
                             |
                             v
                  +----------------------+
                  |     Application      |
                  |      Use Cases       |
                  +----------+-----------+
                             |
                             v
                  +----------------------+
                  |     Unit of Work     |
                  | Repository Contracts |
                  +----------+-----------+
                             |
                             v
                  +----------------------+
                  |    Infrastructure    |
                  |        SQLite        |
                  +----------------------+

Application  --->  Domain
Infrastructure ---> Application
Infrastructure ---> Domain

Domain ---> Python standard library only
```

### Domain

`src/titan/core`

Contains the business model:

- `Investigation`
- `Hypothesis`
- `Evidence`
- `Claim`
- `Interpretation`
- `Thesis`
- `Assessment`
- identifiers and statuses;
- domain events;
- domain invariants and lifecycle behavior.

The domain has no dependency on SQLite, web frameworks, AI providers, or other
external infrastructure.

### Application

`src/titan/application`

Contains application use cases and persistence abstractions.

Mutating use cases operate through `UnitOfWork`, which coordinates investigation
persistence and domain event persistence as a single transaction boundary.

Read-only queries depend on repository abstractions.

### Infrastructure

`src/titan/infrastructure`

Contains concrete infrastructure implementations.

The current implementation provides SQLite-backed:

- investigation persistence;
- hypothesis, evidence, claim, interpretation, thesis, and assessment persistence;
- domain event persistence;
- Unit of Work.

### Composition Root

`src/titan/bootstrap.py`

The composition root connects the application layer to SQLite infrastructure.

`bootstrap(database)` returns a configured `TitanApplication` exposing the
current application use cases.

## Application Usage

A TITAN application can be created against a SQLite database:

```python
from titan.bootstrap import bootstrap
from titan.core.evidence import EvidenceRelationship

application = bootstrap("titan.db")
```

Create an investigation:

```python
investigation = application.create_investigation(
    title="Mars anomaly",
    purpose="Evaluate evidence for microbial activity",
)
```

Activate it:

```python
application.activate_investigation(
    investigation.id,
)
```

Add a hypothesis:

```python
hypothesis = application.add_hypothesis(
    investigation_id=investigation.id,
    statement="Seasonal methane variation indicates microbial activity",
)
```

Add evidence:

```python
evidence = application.add_evidence(
    investigation_id=investigation.id,
    hypothesis_id=hypothesis.id,
    description="Methane concentration varies seasonally",
    source="NASA Curiosity methane measurements",
    relationship=EvidenceRelationship.SUPPORTS,
)
```

Add an atomic claim grounded in that evidence:

```python
claim = application.add_claim(
    investigation_id=investigation.id,
    hypothesis_id=hypothesis.id,
    evidence_id=evidence.id,
    statement="Methane concentration varies seasonally",
)
```

Add an interpretation that explains the claim's relevance:

```python
interpretation = application.add_interpretation(
    investigation_id=investigation.id,
    hypothesis_id=hypothesis.id,
    claim_id=claim.id,
    rationale="Seasonality makes a biological mechanism plausible",
)
```

Confirm the hypothesis:

```python
application.confirm_hypothesis(
    investigation_id=investigation.id,
    hypothesis_id=hypothesis.id,
)
```

Add a provisional thesis:

```python
thesis = application.add_thesis(
    investigation_id=investigation.id,
    statement="Microbial activity is a plausible explanation for the anomaly",
)
```

Add a narrative assessment of that thesis:

```python
assessment = application.add_assessment(
    investigation_id=investigation.id,
    thesis_id=thesis.id,
    narrative=(
        "The thesis is plausible but remains dependent on indirect "
        "seasonal methane evidence"
    ),
)
```

An assessment records an explicit evaluation in words. It does not assign a
verdict, score, confidence percentage, or automatic investment decision.

Close the investigation:

```python
application.close_investigation(
    investigation.id,
)
```

Retrieve the persisted aggregate:

```python
restored = application.get_investigation(
    investigation.id,
)
```

List investigations:

```python
investigations = application.list_investigations()
```

Release application resources when finished:

```python
application.close()
```

The application can be reconstructed against the same SQLite database and the
persisted investigation state, including evidence provenance, relationship
classification, claims, interpretations, provisional theses, and narrative
assessments, will be restored.

## Application Use Cases

The composition root currently exposes:

- `create_investigation`
- `activate_investigation`
- `close_investigation`
- `reopen_investigation`
- `get_investigation`
- `list_investigations`
- `add_hypothesis`
- `remove_hypothesis`
- `confirm_hypothesis`
- `reject_hypothesis`
- `add_evidence`
- `add_claim`
- `add_interpretation`
- `add_thesis`
- `add_assessment`

## Requirements

- Python 3.13
- [uv](https://docs.astral.sh/uv/)

TITAN Core currently has no runtime third-party dependencies.

## Development Setup

Create or synchronize the development environment:

```bash
uv sync
```

Install Git hooks:

```bash
uv run pre-commit install
```

## Validation

Run the complete test suite:

```bash
uv run pytest
```

Run linting:

```bash
uv run ruff check .
```

Check formatting:

```bash
uv run ruff format --check .
```

Run static type checking:

```bash
uv run mypy
```

Run all primary quality gates:

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy
```

## Testing Strategy

The repository contains tests at multiple architectural levels:

```text
tests/
├── core/            Domain behavior and invariants
├── application/     Application use cases
├── infrastructure/  SQLite persistence and Unit of Work
├── architecture/    Dependency boundary enforcement
└── acceptance/      Complete application workflows
```

The acceptance suite verifies a complete persisted workflow through
`bootstrap()`, including application reconstruction against the same SQLite
database.

## Architectural Rules

The project currently enforces two important dependency rules.

### Core isolation

Code under `src/titan/core` may depend only on the Python standard library and
other TITAN Core modules.

### Application persistence boundary

Mutating application use cases use `UnitOfWork` rather than depending directly
on concrete persistence infrastructure.

An architecture test guards direct repository dependencies and requires
intentional exceptions to be explicitly allowlisted.

## Scope

TITAN Core is currently a domain and application foundation.

The project does not currently provide:

- a command-line interface;
- an HTTP API;
- a web framework integration;
- an Event Bus;
- an Outbox;
- AI provider integrations.

Those concerns can be added outside the domain boundary as the platform evolves.

## License

MIT
