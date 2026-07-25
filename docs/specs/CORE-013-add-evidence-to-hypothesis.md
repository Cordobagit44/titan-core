# CORE-013: Add evidence to hypothesis

## User Story

As an investigator,
I want to attach evidence to a hypothesis,
so that I can support or refute it with collected information.

## Acceptance Criteria

- A new entity named `Evidence` exists.
- Evidence contains:
  - `id`
  - `description`
- `Hypothesis` can contain multiple evidence items.
- `Hypothesis.add_evidence()` adds new evidence.
- Evidence is exposed as a read-only collection.
- Existing hypothesis validation remains unchanged.
- Existing investigation behavior remains unchanged.
