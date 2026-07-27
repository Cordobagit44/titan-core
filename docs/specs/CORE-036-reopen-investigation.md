# CORE-036 — Reopen Investigation

## User Story

As a user,
I want to reopen a closed investigation,
so that I can continue working on it.

---

## Acceptance Criteria

- A CLOSED investigation can be reopened.
- Reopening changes the status to ACTIVE.
- Reopening an investigation that is not CLOSED raises an error.
- After reopening, hypotheses can be added and removed again.
- No domain events are introduced in this story.
- No repository or application changes are required.

---

## Technical Notes

A new domain method should be added:

- Investigation.reopen()

Use the following error message when reopening is not allowed:

- investigation is not closed

The existing close() behavior remains unchanged.

---

## Definition of Done

- RED → GREEN → REFACTOR
- Tests added
- Ruff passes
- MyPy passes
- Commit created
