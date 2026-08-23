# CORE-076 — Update README for Evidence Relationships

## Status

Done

## Context

CORE-075 introduced explicit evidence relationship classification through
`EvidenceRelationship`, including `SUPPORTS`, `WEAKENS`, and the legacy
compatibility state `UNSPECIFIED`.

The project README still reflected the state before CORE-075. It reported 142
passing tests and its `add_evidence()` example did not provide the required
relationship argument.

## Goal

Update the README so that the documented application usage matches the current
TITAN Core API and validation state after CORE-075.

## Documentation Changes

The README now:

- reports 147 passing tests;
- imports `EvidenceRelationship` in the application usage example;
- passes an explicit evidence relationship to `add_evidence()`;
- states that persisted application reconstruction preserves evidence provenance
  and evidence relationship classification.

## Acceptance Criteria

- README usage matches the current `AddEvidence` signature.
- README documents `EvidenceRelationship.SUPPORTS` in the evidence example.
- README reports 147 passing tests.
- README states that evidence relationships survive application reconstruction.
- No production behavior changes.
- No runtime dependency changes.
- Existing quality gates remain green.

## Validation

GitHub Actions CI run 42 passed on the CORE-076 pull request branch.

The CI quality job verified:

- Ruff lint;
- Ruff format;
- mypy;
- the complete pytest suite.

## Out of Scope

CORE-076 does not introduce:

- new domain behavior;
- new application behavior;
- new persistence behavior;
- new evidence relationship types;
- evidence weighting or scoring;
- confidence or certainty;
- assessments;
- claims or interpretations;
- CLI or HTTP APIs;
- AI integrations.

## Architectural Notes

CORE-076 is documentation-only. It aligns the public project documentation with
behavior already introduced and validated in CORE-075.
