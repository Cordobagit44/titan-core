# CORE-037 — Record Investigation Closure

## User Story

As a user,
I want to know when an investigation was closed,
so that I have an audit trail of its lifecycle.

---

## Acceptance Criteria

- Closing an investigation records the closing timestamp.
- Reopening an investigation clears the closing timestamp.
- Newly created investigations have no closing timestamp.
- Closing an already closed investigation still raises an error.
- No domain events are introduced.
- Repository changes are not part of this story.

---

## Technical Notes

Add a new attribute to Investigation:

- closed_at: datetime | None

When Investigation.close() is called:

- closed_at is set to the current UTC time.

When Investigation.reopen() is called:

- closed_at becomes None.

Use datetime.now(timezone.utc).

---

## Definition of Done

- RED → GREEN → REFACTOR
- Tests added
- Ruff passes
- MyPy passes
- Commit created
