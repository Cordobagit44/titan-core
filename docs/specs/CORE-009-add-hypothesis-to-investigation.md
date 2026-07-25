# CORE-009 — Add Hypothesis to Investigation

## User Story

As an investment analyst,
I want to add a hypothesis to an investigation,
so that I can record the theses that I want to validate.

## Acceptance Criteria

- An investigation can contain hypotheses.
- A hypothesis is added through the investigation aggregate.
- The investigation creates the hypothesis from a statement.
- The added hypothesis is stored in the investigation.
- The hypotheses collection cannot be modified directly from outside the aggregate.
- Multiple hypotheses may have the same statement for now.

## Technical Notes

- Add an `add_hypothesis` method to `Investigation`.
- The method receives a `statement`.
- The method creates a `Hypothesis`.
- Store hypotheses internally in the aggregate.
- Expose hypotheses as a read-only collection.
- Do not emit a domain event in this story.
