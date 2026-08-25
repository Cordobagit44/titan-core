import sqlite3
from datetime import UTC, datetime

import pytest

from titan.core.assessment import AssessmentId
from titan.core.investigation import AssessmentAdded, InvestigationId
from titan.core.thesis import ThesisId
from titan.infrastructure.sqlite.sqlite_domain_event_repository import (
    SqliteDomainEventRepository,
)


def create_event() -> AssessmentAdded:
    return AssessmentAdded(
        investigation_id=InvestigationId.new(),
        assessment_id=AssessmentId.new(),
        thesis_id=ThesisId.new(),
        recorded_at=datetime(2026, 8, 25, 12, 30, tzinfo=UTC),
    )


def test_sqlite_preserves_assessment_added_recorded_at() -> None:
    repository = SqliteDomainEventRepository(":memory:")
    event = create_event()

    repository.save(event)

    assert repository.list_all() == [event]


def test_missing_assessment_event_timestamp_is_reported() -> None:
    repository = SqliteDomainEventRepository(":memory:")
    event = create_event()
    repository.save(event)
    repository._connection.execute(
        "UPDATE domain_events SET assessment_recorded_at = NULL",
    )

    with pytest.raises(
        ValueError,
        match=("incomplete persisted domain event AssessmentAdded: missing assessment_recorded_at"),
    ):
        repository.list_all()


def test_malformed_assessment_event_timestamp_is_reported() -> None:
    repository = SqliteDomainEventRepository(":memory:")
    event = create_event()
    repository.save(event)
    repository._connection.execute(
        "UPDATE domain_events SET assessment_recorded_at = ?",
        ("not-a-datetime",),
    )

    with pytest.raises(
        ValueError,
        match=("malformed persisted domain event AssessmentAdded: invalid assessment_recorded_at"),
    ):
        repository.list_all()


def test_legacy_assessment_event_receives_explicit_timestamp_marker() -> None:
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
            thesis_id TEXT,
            assessment_id TEXT
        )
        """
    )
    event = create_event()
    connection.execute(
        """
        INSERT INTO domain_events (
            event_type,
            investigation_id,
            thesis_id,
            assessment_id
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            "AssessmentAdded",
            str(event.investigation_id.value),
            str(event.thesis_id.value),
            str(event.assessment_id.value),
        ),
    )

    repository = SqliteDomainEventRepository(connection=connection)
    restored = repository.list_all()[0]

    assert isinstance(restored, AssessmentAdded)
    assert restored.recorded_at == datetime(1970, 1, 1, tzinfo=UTC)
