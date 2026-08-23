# CORE-080 — Close SQLite Test Resources

## Status

Done

## Context

The CI run after CORE-079 completed successfully but reported 26 SQLite
`ResourceWarning` messages. The warnings were surfaced while pytest was running
a bootstrap test, which initially suggested that bootstrap applications were
responsible.

The first CORE-080 change closed those bootstrap applications explicitly, but
the warning count did not change. Further CI diagnosis showed that garbage
collection was reporting connections created earlier by tests, so the warning
location was not the allocation site.

The final CORE-080 implementation added deterministic test cleanup for SQLite
connections while preserving the existing production lifecycle.

## Goal

Ensure test-owned SQLite resources are closed deterministically so the complete
CI test run finishes without SQLite `ResourceWarning` messages.

## Behavior

Bootstrap tests that create a `TitanApplication` close it explicitly.

An autouse pytest fixture tracks real `sqlite3.Connection` objects created by
tests and closes them during teardown. This makes cleanup deterministic even
when the object that owns a connection would otherwise survive until garbage
collection.

Production application cleanup remains explicit through
`TitanApplication.close()` and `SqliteUnitOfWork.close()`.

## Acceptance Criteria

- Bootstrap tests explicitly close applications they create.
- Test-created SQLite connections are closed deterministically.
- Existing application and Unit of Work lifecycle behavior remains unchanged.
- The complete test suite passes without SQLite `ResourceWarning` messages.
- Ruff lint and format checks pass.
- mypy passes.
- No production source code changes.
- No persistence schema changes.
- No runtime dependency changes.

## Out of Scope

CORE-080 does not introduce automatic production cleanup, context-manager
behavior, connection pooling, persistence changes, or new application APIs.

## Architectural Notes

The warning location was a garbage-collection artifact rather than the resource
allocation site. The final correction therefore remains at the test boundary.

The test fixture records connections returned by `sqlite3.connect()` and closes
them after each test. It does not alter transaction semantics, persistence
schemas, or production ownership rules.

## Validation

CORE-080 was integrated to `main` through pull request #5 after its quality
checks passed. The merged change contains no production source modifications.
