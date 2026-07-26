# CORE-018: Add In-Memory Investigation Repository

## User Story

As the application,
I want an in-memory implementation of the investigation repository,
so that investigations can be stored without a database.

## Acceptance Criteria

- An in-memory implementation of `InvestigationRepository` exists.
- Saving an investigation persists it in memory.
- Retrieving an existing investigation returns it.
- Retrieving an unknown investigation returns `None`.
- No existing behavior changes.
