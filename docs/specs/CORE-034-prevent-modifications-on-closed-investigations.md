# CORE-034 — Prevent Modifications on Closed Investigations

## User Story

As a user,
I want closed investigations to become immutable,
so that finalized investigations cannot be modified accidentally.

---

## Acceptance Criteria

- Adding a hypothesis to a closed investigation raises an error.
- Removing a hypothesis from a closed investigation raises an error.
- Activating a closed investigation raises an error.
- Closing an already closed investigation continues to raise an error.
- Repository changes are not required.
- Domain events are not part of this story.

---

## Technical Notes

The Investigation aggregate should reject state-changing operations when its status is CLOSED.

The following methods are affected:

- Investigation.add_hypothesis()
- Investigation.remove_hypothesis()
- Investigation.activate()

Use the error message:

- investigation is closed

The existing behavior of Investigation.close() remains unchanged.

---

## Definition of Done

- RED → GREEN → REFACTOR
- Tests added
- Ruff passes
- MyPy passes
- Commit created
