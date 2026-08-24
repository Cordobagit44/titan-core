# CORE-095 — Prevent Cross-Hypothesis Evidence Reuse

## Status

Done

## Context

CORE-091 prevents duplicate evidence identifiers inside one hypothesis. The
same `Evidence` entity can still be added through the `Investigation` aggregate
to two different hypotheses. That creates two aggregate references to one
identity and later conflicts with SQLite's evidence primary key.

## Goal

Ensure an evidence identifier belongs to at most one hypothesis within an
investigation.

## Acceptance Criteria

- New evidence can still be added to a pending hypothesis.
- Evidence already owned by another hypothesis in the investigation is
  rejected with a domain error.
- Rejected reuse leaves both hypotheses' evidence collections unchanged.
- Rejected reuse emits no new `EvidenceAdded` event.
- Duplicate protection inside the same hypothesis remains unchanged.
- Closed-investigation and decided-hypothesis protections remain unchanged.
- No public signature, schema, event type, or dependency changes.
- The complete test suite and quality gates pass.

## Out of Scope

- Sharing one evidence identity across hypotheses.
- Copying evidence with a new identifier.
- Semantic duplicate detection by description or source.
- Cross-investigation evidence identity rules.

## Architectural Notes

Cross-hypothesis ownership is an aggregate invariant and therefore belongs to
`Investigation.add_evidence()`. `Hypothesis` retains its local identity and
decision-state protections.

## Validation

- Targeted investigation evidence tests — 4 passed
- pytest — 189 passed
- Ruff lint — passed
- Ruff format — 175 files already formatted
- mypy — 65 source files checked
