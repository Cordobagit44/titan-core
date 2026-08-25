import sqlite3

import pytest

from titan.core.assessment import Assessment
from titan.core.investigation import AssessmentAdded, Investigation
from titan.core.thesis import Thesis
from titan.infrastructure.sqlite.sqlite_domain_event_repository import (
    SqliteDomainEventRepository,
)


def create_assessment_added_event() -> AssessmentAdded:
    investigation = Investigation.create("Mars anomaly", "Evaluate evidence")
    thesis = Thesis(statement="The anomaly is geological.")
    investigation.add_thesis(thesis)
    investigation.pull_events()
    assessment = Assessment(
        thesis_id=thesis.id,
        narrative="The evidence supports the thesis with limitations.",
    )
    investigation.add_assessment(assessment)
    event = investigation.pull_events()[0]
    assert isinstance(event, AssessmentAdded)
    return event


def test_save_and_list_assessment_added_event() -> None:
    repository = SqliteDomainEventRepository(":memory:")
    event = create_assessment_added_event()

    repository.save(event)

    assert repository.list_all() == [event]


def test_existing_event_schema_gains_assessment_id_column() -> None:
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
            interpretation_id TEXT,
            thesis_id TEXT
        )
        """
    )

    SqliteDomainEventRepository(connection=connection)

    columns = {row[1] for row in connection.execute("PRAGMA table_info(domain_events)").fetchall()}
    assert "assessment_id" in columns


def test_incomplete_assessment_added_event_is_rejected() -> None:
    connection = sqlite3.connect(":memory:")
    repository = SqliteDomainEventRepository(connection=connection)
    event = create_assessment_added_event()
    connection.execute(
        """
        INSERT INTO domain_events (event_type, investigation_id, thesis_id)
        VALUES (?, ?, ?)
        """,
        (
            "AssessmentAdded",
            str(event.investigation_id.value),
            str(event.thesis_id.value),
        ),
    )

    with pytest.raises(
        ValueError,
        match="incomplete persisted domain event AssessmentAdded: missing assessment_id",
    ):
        repository.list_all()


def test_malformed_assessment_added_id_is_reported() -> None:
    connection = sqlite3.connect(":memory:")
    repository = SqliteDomainEventRepository(connection=connection)
    event = create_assessment_added_event()
    connection.execute(
        """
        INSERT INTO domain_events (
            event_type, investigation_id, thesis_id, assessment_id
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            "AssessmentAdded",
            str(event.investigation_id.value),
            str(event.thesis_id.value),
            "not-a-uuid",
        ),
    )

    with pytest.raises(
        ValueError,
        match="malformed persisted domain event AssessmentAdded: invalid assessment_id",
    ):
        repository.list_all()
