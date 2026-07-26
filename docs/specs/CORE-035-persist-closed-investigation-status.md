# CORE-035 — Persist Closed Investigation Status

## User Story

As a user,
I want the CLOSED status of an investigation to be persisted,
so that closed investigations remain closed after being reloaded.

---

## Acceptance Criteria

- CLOSED investigations are persisted correctly.
- Restoring a CLOSED investigation returns it with status CLOSED.
- Existing persistence behavior for DRAFT and ACTIVE remains unchanged.
- No application-layer changes are required.

---

## Technical Notes

The SQLite repository already persists investigation status.

This story extends persistence to support the new InvestigationStatus value:

- CLOSED

Tests should verify round-trip persistence.

---

## Definition of Done

- RED → GREEN → REFACTOR
- Tests added
- Ruff passes
- MyPy passes
- Commit created
