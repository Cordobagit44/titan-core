# CORE-033 — Close Investigation

## User Story

As a user,
I want to close an investigation,
so that it can no longer be modified.

---

## Acceptance Criteria

- Investigation can be closed.
- Status becomes CLOSED.
- Closing an already closed investigation raises an error.
- Active and draft investigations can be closed.
- Domain events are not part of this story.

---

## Technical Notes

A new InvestigationStatus value should be introduced:

- CLOSED

A new domain method should be added:

- Investigation.close()

No repository or application changes are required in this story.

---

## Definition of Done

- RED → GREEN → REFACTOR
- Tests added
- Ruff passes
- MyPy passes
- Commit created
