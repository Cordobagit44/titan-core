import sqlite3

import pytest

from titan.core.investigation import Investigation, ThesisAdded
from titan.core.thesis import Thesis
from titan.infrastructure.sqlite.sqlite_domain_event_repository import (
    SqliteDomainEventRepository,
)


def create_thesis_added_event() -> ThesisAdded:
    investigation = Investigation.create("Mars anomaly", "Evaluate evidence")
    investigation.pull_events()
    investigation.add_thesis(Thesis(statement="The anomaly is geological."))
    event = investigation.pull_events()[0]
    assert isinstance(event, ThesisAdded)
    return event


def test_save_and_list_thesis_added_event() -> None:
    repository = SqliteDomainEventRepository(":memory:")
    event = create_thesis_added_event()

    repository.save(event)

    assert repository.list_all() == [event]


def test_existing_event_schema_gains_thesis_id_column() -> None:
    connection = sqlite3.connect(":memory:")
    connection.execute(
        """
        CREATE TABLE domain_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT NOT NULL,
            investigation_id TEXT,
            title TEXT,
            closed_at TEXT,
            hypothesis_statement TEXT,
            hypothesis_id TEXT,
            evidence_id TEXT,
            claim_id TEXT,
            interpretation_id TEXT
        )
        """
    )

    SqliteDomainEventRepository(connection=connection)

    columns = {
        row[1] for row in connection.execute("PRAGMA table_info(domain_events)").fetchall()
    }
    assert "thesis_id" in columns


def test_incomplete_thesis_added_event_is_rejected() -> None:
    connection = sqlite3.connect(":memory:")
    repository = SqliteDomainEventRepository(connection=connection)
    event = create_thesis_added_event()
    connection.execute(
        """
        INSERT INTO domain_events (event_type, investigation_id)
        VALUES (?, ?)
        """,
        ("ThesisAdded", str(event.investigation_id.value)),
    )

    with pytest.raises(
        ValueError,
        match="incomplete persisted domain event ThesisAdded: missing thesis_id",
    ):
        repository.list_all()


def test_malformed_thesis_added_id_is_reported() -> None:
    connection = sqlite3.connect(":memory:")
    repository = SqliteDomainEventRepository(connection=connection)
    event = create_thesis_added_event()
    connection.execute(
        """
        INSERT INTO domain_events (event_type, investigation_id, thesis_id)
        VALUES (?, ?, ?)
        """,
        ("ThesisAdded", str(event.investigation_id.value), "not-a-uuid"),
    )

    with pytest.raises(
        ValueError,
        match="malformed persisted domain event ThesisAdded: invalid thesis_id",
    ):
        repository.list_all()
