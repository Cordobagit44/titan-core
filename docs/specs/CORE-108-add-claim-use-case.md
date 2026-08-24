# CORE-108 — Add Claim Use Case

## Status

Done

## Context

The domain, aggregate repository, and event store now support claims, but no
application operation coordinates claim creation and persistence atomically.

## Goal

Introduce a transactional `AddClaim` application use case and expose it from
the composition root.

## Acceptance Criteria

- The use case accepts investigation, hypothesis, evidence IDs, and statement.
- It returns the created `Claim` with a generated identity.
- Mutation routes through `Investigation.add_claim()`.
- Successful execution saves aggregate state and persists `ClaimAdded`.
- Successful execution commits exactly through the Unit of Work boundary.
- Missing investigation, unknown hypothesis/evidence, closed investigation,
  decided hypothesis, invalid statement, and persistence failure roll back.
- `bootstrap()` exposes `add_claim`.
- Existing use cases and transaction behavior remain intact.
- The complete test suite and quality gates pass.

## Out of Scope

- Claim removal or editing.
- Interpretation, assessment, confidence, or thesis behavior.
- Automatic claim extraction or AI integration.
- HTTP or CLI interfaces.

## Architectural Notes

The application layer creates the claim, the aggregate enforces ownership and
lifecycle, and Unit of Work coordinates aggregate and event persistence.

## Validation

- Targeted AddClaim and bootstrap tests — 7 passed
- pytest — 232 passed
- Ruff lint — passed
- Ruff format — 194 files already formatted
- mypy — 71 source files checked
