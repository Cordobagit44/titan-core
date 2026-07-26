# CORE-032 — Persist Hypothesis Evidences

## User Story

As a user,
I want hypothesis evidences to be persisted,
so that investigations can be fully restored from SQLite.

---

## Acceptance Criteria

- SQLite repository persists every Evidence belonging to every Hypothesis.
- Saving an Investigation stores all evidences.
- Restoring an Investigation restores evidences for every hypothesis.
- Listing Investigations restores evidences as well.
- No domain events are emitted during rehydration.
- Existing tests continue to pass.

---

## Technical Notes

A new SQLite table should be introduced:

- evidences

Suggested columns:

- id INTEGER PRIMARY KEY
- investigation_id TEXT NOT NULL
- hypothesis_id TEXT NOT NULL
- source TEXT NOT NULL
- summary TEXT NOT NULL

The repository should:

- delete existing evidences for an investigation before inserting the current state
- restore evidences after restoring hypotheses
- preserve aggregate consistency during rehydration

---

## Definition of Done

- RED → GREEN → REFACTOR
- Tests added
- Ruff passes
- MyPy passes
- Commit created
