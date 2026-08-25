import sqlite3
from datetime import UTC, datetime

import pytest

from titan.core.assessment import Assessment
from titan.core.investigation import Investigation
from titan.core.thesis import Thesis
from titan.infrastructure.sqlite.sqlite_investigation_repository import (
    SqliteInvestigationRepository,
)


def create_investigation_with_assessment(
    recorded_at: datetime,
) -> tuple[Investigation, Assessment]:
    investigation = Investigation.create("Mars anomaly", "Evaluate evidence")
    thesis = Thesis(statement="The anomaly is geological.")
    investigation.add_thesis(thesis)
    assessment = Assessment(
        thesis_id=thesis.id,
        narrative="The thesis is plausible but remains provisional.",
        recorded_at=recorded_at,
    )
    investigation.add_assessment(assessment)
    return investigation, assessment


def test_sqlite_preserves_assessment_recorded_at() -> None:
    repository = SqliteInvestigationRepository(":memory:")
    recorded_at = datetime(2026, 8, 25, 12, 30, tzinfo=UTC)
    investigation, assessment = create_investigation_with_assessment(recorded_at)

    repository.save(investigation)

    restored = repository.get(investigation.id)

    assert restored is not None
    assert restored.assessments[0].id == assessment.id
    assert restored.assessments[0].recorded_at == recorded_at


def test_legacy_assessment_schema_receives_explicit_timestamp_marker() -> None:
    connection = sqlite3.connect(":memory:")
    connection.execute(
        """
        CREATE TABLE assessments (
            id TEXT PRIMARY KEY,
            investigation_id TEXT NOT NULL,
            thesis_id TEXT NOT NULL,
            narrative TEXT NOT NULL
        )
        """
    )

    SqliteInvestigationRepository(connection=connection)

    columns = {
        row[1]: row
        for row in connection.execute(
            "PRAGMA table_info(assessments)",
        ).fetchall()
    }

    assert "recorded_at" in columns
    assert columns["recorded_at"][4] == "'1970-01-01T00:00:00+00:00'"


def test_malformed_persisted_assessment_recorded_at_is_reported() -> None:
    repository = SqliteInvestigationRepository(":memory:")
    investigation, assessment = create_investigation_with_assessment(
        datetime(2026, 8, 25, 12, 30, tzinfo=UTC),
    )
    repository.save(investigation)
    repository._connection.execute(
        "UPDATE assessments SET recorded_at = ? WHERE id = ?",
        ("not-a-datetime", str(assessment.id.value)),
    )

    with pytest.raises(
        ValueError,
        match=f"malformed persisted assessment {assessment.id.value}: invalid recorded_at",
    ):
        repository.get(investigation.id)
