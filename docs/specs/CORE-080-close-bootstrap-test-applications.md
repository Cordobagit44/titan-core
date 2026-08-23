# CORE-080 — Close Bootstrap Test Applications

## Status

In Progress

## Context

The CI run for CORE-079 completed successfully but reported SQLite
`ResourceWarning` messages from bootstrap tests that create a `TitanApplication`
without closing it.

`TitanApplication.close()` already exists and releases the shared SQLite Unit of
Work connection. The affected tests are not exercising lifecycle cleanup and
therefore leave test resources open until garbage collection.

## Goal

Make bootstrap tests release application resources explicitly so the complete
CI test run finishes without SQLite resource warnings.

## Behavior

Tests that call `bootstrap()` and do not intentionally verify behavior after
closure must call `application.close()` before finishing.

No production lifecycle behavior changes are required.

## Acceptance Criteria

- Bootstrap tests explicitly close applications they create.
- The existing application-close test continues to verify closed-resource behavior.
- The complete test suite passes without SQLite `ResourceWarning` messages.
- Ruff lint and format checks pass.
- mypy passes.
- No production source code changes.
- No persistence schema changes.
- No runtime dependency changes.

## Out of Scope

CORE-080 does not introduce automatic cleanup, context-manager behavior,
connection pooling, persistence changes, or new application APIs.

## Architectural Notes

This is test-resource hygiene. Explicit lifecycle management already exists in
production through `TitanApplication.close()`; tests should respect that same
boundary rather than relying on garbage collection.
