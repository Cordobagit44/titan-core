# CORE-030: Persist Investigation Status

## User Story

As the application,
I want investigation status to be persisted,
so that loaded investigations preserve their lifecycle.

## Acceptance Criteria

- SQLite stores investigation status.
- save() persists status.
- get() restores status.
- list() restores status.
- Existing behavior remains unchanged.
