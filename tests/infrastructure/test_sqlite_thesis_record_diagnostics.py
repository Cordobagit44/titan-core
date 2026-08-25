import sqlite3
from uuid import UUID, uuid4

import pytest

from titan.core.investigation import InvestigationId
from titan.infrastructure.sqlite.sqlite_investigation_repository import (
    SqliteInvestigationRepository,
)


def insert_investigation(connection: sqlite3.Connection, investigation_id: str) -> None:
    connection.execute(
        """
        INSERT INTO investigations (id, title, purpose, status, closed_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (investigation_id, "Mars anomaly", "Evaluate evidence", "draft", None),
    )


def test_malformed_persisted_thesis_id_is_reported() -> None:
    connection = sqlite3.connect(":memory:")
    repository = SqliteInvestigationRepository(connection=connection)
    investigation_id = str(uuid4())
    insert_investigation(connection, investigation_id)
    connection.execute(
        """
        INSERT INTO theses (id, investigation_id, statement)
        VALUES (?, ?, ?)
        """,
        ("not-a-uuid", investigation_id, "A valid statement"),
    )

    with pytest.raises(
        ValueError,
        match="malformed persisted thesis record: invalid id",
    ):
        repository.get(InvestigationId(value=UUID(investigation_id)))


def test_blank_persisted_thesis_statement_is_reported() -> None:
    connection = sqlite3.connect(":memory:")
    repository = SqliteInvestigationRepository(connection=connection)
    investigation_id = str(uuid4())
    thesis_id = str(uuid4())
    insert_investigation(connection, investigation_id)
    connection.execute(
        """
        INSERT INTO theses (id, investigation_id, statement)
        VALUES (?, ?, ?)
        """,
        (thesis_id, investigation_id, "   "),
    )

    with pytest.raises(
        ValueError,
        match=f"malformed persisted thesis {thesis_id}: invalid statement",
    ):
        repository.get(InvestigationId(value=UUID(investigation_id)))
