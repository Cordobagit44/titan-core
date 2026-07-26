# CORE-006 — Activate Investigation

## User Story

As an analyst,
I want to activate a draft investigation,
so that the system records that research has officially started.

## Acceptance Criteria

- A newly created investigation starts in `DRAFT`.
- Calling `activate()` changes the status to `ACTIVE`.
- Activating an already active investigation raises `ValueError`.
- The error message is `investigation is already active`.

## Technical Notes

- Add `ACTIVE` to `InvestigationStatus`.
- Add behavior to the `Investigation` aggregate.
- The aggregate must protect the state transition.
