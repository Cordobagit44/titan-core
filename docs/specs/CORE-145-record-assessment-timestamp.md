# CORE-145 — Record Assessment Timestamp

## Context

Narrative assessments can be persisted and reconstructed, but they do not
record when the evaluation was formulated. Living financial research needs an
explicit time anchor so later evaluations can be distinguished historically.

## Goal

Add an immutable UTC-aware `recorded_at` timestamp to assessments and preserve
it through SQLite.

## Acceptance Criteria

- New assessments receive a timezone-aware UTC `recorded_at` value.
- Explicit timestamps are accepted for deterministic reconstruction.
- SQLite saves and restores the exact timestamp.
- Existing assessment tables are migrated with an explicit legacy timestamp
  marker rather than silently dropping records.
- Malformed persisted timestamps identify the assessment and field.
- The public application call remains unchanged.
- No verdict, score, confidence value, or automatic decision is introduced.
- The complete quality gates pass.

## Out of Scope

- Editing or superseding assessments.
- User-supplied timestamps through the application API.
- Time-based scoring or automatic investment decisions.
- HTTP, CLI, UI, or AI integration.

## Architectural Notes

The timestamp belongs to the immutable assessment fact. SQLite stores ISO 8601
text. Legacy records use the Unix epoch in UTC as an explicit unknown-history
marker.

## Validation

Pending implementation and CI.
