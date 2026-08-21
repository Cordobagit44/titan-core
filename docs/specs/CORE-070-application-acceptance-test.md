# CORE-070 — Add Application Acceptance Test

## Status

Done

## Context

TITAN Core now provides a complete application composition root backed by
SQLite.

Domain, application, infrastructure, and architecture tests already cover the
system at their respective boundaries, but there is no acceptance test proving
that a complete investigation workflow works through the composed application.

## Goal

Add an acceptance test that exercises a complete investigation workflow through
the public application composition root and verifies that the resulting state
survives application reconstruction.

## Acceptance Criteria

- Exercise the application through `bootstrap()`.
- Create an investigation.
- Activate the investigation.
- Add a hypothesis.
- Add evidence to the hypothesis.
- Confirm the hypothesis.
- Close the investigation.
- Reconstruct the application using the same SQLite database.
- Retrieve the persisted investigation.
- Verify the persisted investigation state.
- Verify the persisted hypothesis state.
- Verify the persisted evidence.
- Verify the investigation appears in the application query results.
- Do not access repositories directly from the acceptance test.
- Do not modify production behavior unless the acceptance test exposes a real
  integration defect.

## Architectural Notes

The acceptance test exercises the complete path:

`composition root -> application use cases -> Unit of Work -> SQLite -> aggregate reconstruction -> queries`

The test interacts with TITAN through the application composition root rather
than directly through infrastructure components.

Reconstructing the application against the same SQLite database verifies that
the result does not depend on in-memory object identity or process-local state.

No production code change was required.

## Test Coverage

The acceptance scenario verifies:

- investigation creation;
- investigation activation;
- hypothesis creation;
- evidence creation;
- hypothesis confirmation;
- investigation closure;
- SQLite persistence across application reconstruction;
- aggregate reconstruction;
- investigation retrieval;
- investigation listing.

## Validation

- pytest — 136 passed
- Ruff — passed
- mypy — 60 source files checked
