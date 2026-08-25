import sqlite3
from uuid import UUID, uuid4

import pytest

from titan.core.investigation import InvestigationId
from titan.infrastructure.sqlite.sqlite_investigation_repository import (
    SqliteInvestigationRepository,
)


def test_persisted_assessment_with_unknown_thesis_is_reported() -> None:
    connection = sqlite3.connect(":memory:")
    repository = SqliteInvestigationRepository(connection=connection)
    investigation_id = str(uuid4())
    assessment_id = str(uuid4())
    connection.execute(
        """
        INSERT INTO investigations (id, title, purpose, status, closed_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (investigation_id, "Mars anomaly", "Evaluate evidence", "draft", None),
    )
    connection.execute(
        """
        INSERT INTO assessments (id, investigation_id, thesis_id, narrative)
        VALUES (?, ?, ?, ?)
        """,
        (
            assessment_id,
            investigation_id,
            str(uuid4()),
            "The evidence remains incomplete.",
        ),
    )

    with pytest.raises(
        ValueError,
        match=f"malformed persisted assessment {assessment_id}: thesis not found",
    ):
        repository.get(InvestigationId(value=UUID(investigation_id)))
