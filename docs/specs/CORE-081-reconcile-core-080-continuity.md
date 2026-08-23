# CORE-081 — Reconcile CORE-080 Continuity

## Status

Done

## Context

CORE-080 was merged after adding deterministic SQLite connection cleanup for
tests, but its continuity documentation did not catch up with the final
implementation.

The merged implementation includes an autouse test fixture that tracks SQLite
connections and closes them after each test. The CORE-080 specification still
described only the initial bootstrap-cleanup hypothesis, and `BACKLOG.md` still
identified CORE-079 as the latest completed story.

This mismatch made repository recovery less reliable even though the code in
`main` was ahead of the documentation.

## Goal

Restore the repository as a trustworthy recovery point by documenting the
actual completed CORE-080 behavior and recording the corrected continuity state.

## Documentation Changes

CORE-081:

- corrected the CORE-080 specification to describe the final SQLite test-resource
  cleanup and marked CORE-080 `Done`;
- recorded CORE-080 as completed in `BACKLOG.md`;
- recorded CORE-081 during the repair and, after validation, marked it complete;
- preserved the distinction between test-only resource cleanup and production
  lifecycle behavior.

## Acceptance Criteria

- CORE-080 documentation matches the implementation merged to `main`.
- `BACKLOG.md` no longer identifies CORE-079 as the latest completed story.
- CORE-081 is recorded as completed after successful validation.
- No production source code changes.
- No persistence schema changes.
- No runtime dependency changes.
- The complete test suite passes without SQLite `ResourceWarning` messages.
- Ruff lint and format checks pass.
- mypy passes.

## Validation

GitHub Actions CI run 69 passed on the CORE-081 pull request branch.

The CI quality job verified:

- Ruff lint passed;
- Ruff format check passed;
- mypy passed on 65 source files;
- pytest passed with 159 tests;
- the pytest run completed without a SQLite `ResourceWarning` summary.

## Out of Scope

CORE-081 does not introduce new domain, application, persistence, or runtime
behavior. It does not add connection pooling, automatic production cleanup, new
APIs, or new dependencies.

## Architectural Notes

Continuity documentation is a development-safety mechanism in TITAN. When a
story evolves after an initial hypothesis is disproved, the final repository
state must record the corrected diagnosis rather than preserve an obsolete
intermediate explanation.
