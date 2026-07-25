# CORE-014: Introduce hypothesis status

## User Story

As an investigator,
I want to confirm or reject a hypothesis,
so that I can record the outcome of the investigation.

## Acceptance Criteria

- A `HypothesisStatus` enum exists.
- The available statuses are:
  - `PENDING`
  - `CONFIRMED`
  - `REJECTED`
- A new hypothesis starts with status `PENDING`.
- `Hypothesis.confirm()` changes the status to `CONFIRMED`.
- `Hypothesis.reject()` changes the status to `REJECTED`.
- A rejected hypothesis cannot be confirmed.
- A confirmed hypothesis cannot be rejected.
- Existing hypothesis validation remains unchanged.
- Existing evidence behavior remains unchanged.
- Existing investigation behavior remains unchanged.
