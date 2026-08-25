import sqlite3
from uuid import UUID, uuid4

import pytest

from titan.core.investigation import InvestigationId
from titan.infrastructure.sqlite.sqlite_investigation_repository import (
    SqliteInvestigationRepository,
)


def insert_investigation_and_thesis(
    connection: sqlite3.Connection,
    investigation_id: str,
    thesis_id: str,
) -> None:
    connection.execute(
        """
        INSERT INTO investigations (id, title, purpose, status, closed_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (investigation_id, "Mars anomaly", "Evaluate evidence", "draft", None),
    )
    connection.execute(
        """
        INSERT INTO theses (id, investigation_id, statement)
        VALUES (?, ?, ?)
        """,
        (thesis_id, investigation_id, "A provisional thesis"),
    )


def test_malformed_persisted_assessment_id_is_reported() -> None:
    connection = sqlite3.connect(":memory:")
    repository = SqliteInvestigationRepository(connection=connection)
    investigation_id = str(uuid4())
    thesis_id = str(uuid4())
    insert_investigation_and_thesis(connection, investigation_id, thesis_id)
    connection.execute(
        """
        INSERT INTO assessments (id, investigation_id, thesis_id, narrative)
        VALUES (?, ?, ?, ?)
        """,
        ("not-a-uuid", investigation_id, thesis_id, "A valid narrative"),
    )

    with pytest.raises(
        ValueError,
        match="malformed persisted assessment record: invalid id",
    ):
        repository.get(InvestigationId(value=UUID(investigation_id)))


def test_malformed_persisted_assessment_thesis_id_is_reported() -> None:
    connection = sqlite3.connect(":memory:")
    repository = SqliteInvestigationRepository(connection=connection)
    investigation_id = str(uuid4())
    thesis_id = str(uuid4())
    assessment_id = str(uuid4())
    insert_investigation_and_thesis(connection, investigation_id, thesis_id)
    connection.execute(
        """
        INSERT INTO assessments (id, investigation_id, thesis_id, narrative)
        VALUES (?, ?, ?, ?)
        """,
        (assessment_id, investigation_id, "not-a-uuid", "A valid narrative"),
    )

    with pytest.raises(
        ValueError,
        match=f"malformed persisted assessment {assessment_id}: invalid thesis_id",
    ):
        repository.get(InvestigationId(value=UUID(investigation_id)))


def test_blank_persisted_assessment_narrative_is_reported() -> None:
    connection = sqlite3.connect(":memory:")
    repository = SqliteInvestigationRepository(connection=connection)
    investigation_id = str(uuid4())
    thesis_id = str(uuid4())
    assessment_id = str(uuid4())
    insert_investigation_and_thesis(connection, investigation_id, thesis_id)
    connection.execute(
        """
        INSERT INTO assessments (id, investigation_id, thesis_id, narrative)
        VALUES (?, ?, ?, ?)
        """,
        (assessment_id, investigation_id, thesis_id, "   "),
    )

    with pytest.raises(
        ValueError,
        match=f"malformed persisted assessment {assessment_id}: invalid narrative",
    ):
        repository.get(InvestigationId(value=UUID(investigation_id)))
