# CORE-031: Persist Investigation Hypotheses

## User Story

As the application,
I want investigation hypotheses to be persisted,
so that loaded investigations preserve their hypotheses.

## Acceptance Criteria

- SQLite stores hypotheses associated with an investigation.
- `save()` persists the investigation hypotheses.
- `get()` restores the investigation hypotheses.
- `list()` restores the investigation hypotheses.
- Saving an investigation replaces its previously persisted hypothesis state.
- Loading an investigation does not produce new domain events.
- Existing application use cases remain unchanged.
- Existing behavior remains unchanged.

## Technical Notes

- Use the standard `sqlite3` module.
- Add a separate `hypotheses` table.
- Associate hypotheses with their investigation through `investigation_id`.
- Do not persist evidence in this story.
- Do not introduce an ORM.
- Do not introduce migrations yet.
