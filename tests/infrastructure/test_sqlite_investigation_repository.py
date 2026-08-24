import sqlite3
from pathlib import Path

import pytest

from titan.core.evidence import (
    Evidence,
    EvidenceRelationship,
)
from titan.core.investigation import Investigation
from titan.infrastructure.sqlite.sqlite_investigation_repository import (
    SqliteInvestigationRepository,
)


def test_save_and_get_investigation() -> None:
    repository = SqliteInvestigationRepository(
        ":memory:",
    )

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    repository.save(
        investigation,
    )

    found = repository.get(
        investigation.id,
    )

    assert found is not None
    assert found.id == investigation.id
    assert found.title == investigation.title
    assert found.purpose == investigation.purpose


def test_list_investigations() -> None:
    repository = SqliteInvestigationRepository(
        ":memory:",
    )

    first_investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    second_investigation = Investigation.create(
        title="Ocean signal",
        purpose="Identify its origin",
    )

    repository.save(
        first_investigation,
    )
    repository.save(
        second_investigation,
    )

    investigations = repository.list()

    assert len(investigations) == 2
    assert investigations[0].id == first_investigation.id
    assert investigations[1].id == second_investigation.id


def test_get_restores_investigation_status() -> None:
    repository = SqliteInvestigationRepository(
        ":memory:",
    )

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    investigation.activate()

    repository.save(
        investigation,
    )

    found = repository.get(
        investigation.id,
    )

    assert found is not None
    assert found.status == investigation.status


def test_get_restores_hypotheses() -> None:
    repository = SqliteInvestigationRepository(
        ":memory:",
    )

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    investigation.add_hypothesis(
        "Artificial structure",
    )

    repository.save(
        investigation,
    )

    found = repository.get(
        investigation.id,
    )

    assert found is not None
    assert len(found.hypotheses) == 1
    assert found.hypotheses[0].statement == "Artificial structure"


def test_list_restores_hypotheses() -> None:
    repository = SqliteInvestigationRepository(
        ":memory:",
    )

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    investigation.add_hypothesis(
        "Artificial structure",
    )

    repository.save(
        investigation,
    )

    investigations = repository.list()

    assert len(investigations) == 1
    assert len(investigations[0].hypotheses) == 1
    assert investigations[0].hypotheses[0].statement == "Artificial structure"


def test_get_restores_supporting_hypothesis_evidence() -> None:
    repository = SqliteInvestigationRepository(
        ":memory:",
    )

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    investigation.add_hypothesis(
        "Artificial structure",
    )

    hypothesis = investigation.hypotheses[0]

    hypothesis.add_evidence(
        Evidence(
            description="High-resolution orbital imagery",
            source="Mars Reconnaissance Orbiter imagery",
            relationship=EvidenceRelationship.SUPPORTS,
        )
    )

    repository.save(
        investigation,
    )

    found = repository.get(
        investigation.id,
    )

    assert found is not None
    assert len(found.hypotheses) == 1
    assert len(found.hypotheses[0].evidences) == 1

    restored_evidence = found.hypotheses[0].evidences[0]

    assert restored_evidence.description == "High-resolution orbital imagery"
    assert restored_evidence.source == "Mars Reconnaissance Orbiter imagery"
    assert restored_evidence.relationship is EvidenceRelationship.SUPPORTS


def test_get_restores_weakening_hypothesis_evidence() -> None:
    repository = SqliteInvestigationRepository(
        ":memory:",
    )

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    investigation.add_hypothesis(
        "Artificial structure",
    )

    hypothesis = investigation.hypotheses[0]

    hypothesis.add_evidence(
        Evidence(
            description="Geological process explains the observed structure",
            source="Planetary geology analysis",
            relationship=EvidenceRelationship.WEAKENS,
        )
    )

    repository.save(
        investigation,
    )

    found = repository.get(
        investigation.id,
    )

    assert found is not None
    assert len(found.hypotheses) == 1
    assert len(found.hypotheses[0].evidences) == 1

    restored_evidence = found.hypotheses[0].evidences[0]

    assert restored_evidence.description == "Geological process explains the observed structure"
    assert restored_evidence.source == "Planetary geology analysis"
    assert restored_evidence.relationship is EvidenceRelationship.WEAKENS


def test_save_removes_evidence_for_removed_hypothesis() -> None:
    connection = sqlite3.connect(":memory:")
    repository = SqliteInvestigationRepository(
        connection=connection,
    )
    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    investigation.add_hypothesis(
        "Artificial structure",
    )
    hypothesis = investigation.hypotheses[0]
    hypothesis.add_evidence(
        Evidence(
            description="High-resolution orbital imagery",
            source="Mars Reconnaissance Orbiter imagery",
            relationship=EvidenceRelationship.SUPPORTS,
        )
    )
    repository.save(investigation)

    other_investigation = Investigation.create(
        title="Ocean signal",
        purpose="Identify its origin",
    )
    other_investigation.add_hypothesis(
        "The signal is artificial",
    )
    other_hypothesis = other_investigation.hypotheses[0]
    other_hypothesis.add_evidence(
        Evidence(
            description="The signal repeats at exact intervals",
            source="Hydrophone array",
            relationship=EvidenceRelationship.SUPPORTS,
        )
    )
    repository.save(other_investigation)

    investigation.remove_hypothesis(hypothesis.id)
    repository.save(investigation)

    evidence_rows = connection.execute(
        "SELECT hypothesis_id FROM evidences",
    ).fetchall()

    assert evidence_rows == [(str(other_hypothesis.id.value),)]


def test_legacy_evidence_schema_is_migrated(
    tmp_path: Path,
) -> None:
    database = str(
        tmp_path / "legacy_investigations.db",
    )

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    investigation.add_hypothesis(
        "Artificial structure",
    )

    hypothesis = investigation.hypotheses[0]

    evidence = Evidence(
        description="High-resolution orbital imagery",
        source="Source unavailable in legacy schema",
        relationship=EvidenceRelationship.UNSPECIFIED,
    )

    connection = sqlite3.connect(
        database,
    )

    connection.execute(
        """
        CREATE TABLE investigations (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            purpose TEXT NOT NULL,
            status TEXT NOT NULL,
            closed_at TEXT
        )
        """
    )

    connection.execute(
        """
        CREATE TABLE hypotheses (
            id TEXT PRIMARY KEY,
            investigation_id TEXT NOT NULL,
            statement TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (investigation_id)
                REFERENCES investigations (id)
        )
        """
    )

    connection.execute(
        """
        CREATE TABLE evidences (
            id TEXT PRIMARY KEY,
            hypothesis_id TEXT NOT NULL,
            description TEXT NOT NULL,
            FOREIGN KEY (hypothesis_id)
                REFERENCES hypotheses (id)
        )
        """
    )

    connection.execute(
        """
        INSERT INTO investigations (
            id,
            title,
            purpose,
            status,
            closed_at
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            str(investigation.id.value),
            investigation.title,
            investigation.purpose,
            investigation.status.value,
            None,
        ),
    )

    connection.execute(
        """
        INSERT INTO hypotheses (
            id,
            investigation_id,
            statement,
            status
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            str(hypothesis.id.value),
            str(investigation.id.value),
            hypothesis.statement,
            hypothesis.status.value,
        ),
    )

    connection.execute(
        """
        INSERT INTO evidences (
            id,
            hypothesis_id,
            description
        )
        VALUES (?, ?, ?)
        """,
        (
            str(evidence.id.value),
            str(hypothesis.id.value),
            evidence.description,
        ),
    )

    connection.commit()
    connection.close()

    repository = SqliteInvestigationRepository(
        database,
    )

    restored = repository.get(
        investigation.id,
    )

    assert restored is not None
    assert len(restored.hypotheses) == 1
    assert len(restored.hypotheses[0].evidences) == 1

    restored_evidence = restored.hypotheses[0].evidences[0]

    assert restored_evidence.id == evidence.id
    assert restored_evidence.description == evidence.description
    assert restored_evidence.source == "legacy source unavailable"
    assert restored_evidence.relationship is EvidenceRelationship.UNSPECIFIED


def test_legacy_investigation_schema_is_migrated() -> None:
    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    connection = sqlite3.connect(":memory:")
    connection.execute(
        """
        CREATE TABLE investigations (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            purpose TEXT NOT NULL,
            status TEXT NOT NULL
        )
        """
    )
    connection.execute(
        """
        INSERT INTO investigations (id, title, purpose, status)
        VALUES (?, ?, ?, ?)
        """,
        (
            str(investigation.id.value),
            investigation.title,
            investigation.purpose,
            investigation.status.value,
        ),
    )

    repository = SqliteInvestigationRepository(
        connection=connection,
    )
    restored = repository.get(investigation.id)
    columns = {
        row[1]
        for row in connection.execute(
            "PRAGMA table_info(investigations)",
        ).fetchall()
    }

    assert "closed_at" in columns
    assert restored is not None
    assert restored.id == investigation.id
    assert restored.closed_at is None


def test_get_restores_closed_investigation_status() -> None:
    repository = SqliteInvestigationRepository(
        ":memory:",
    )

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    investigation.close()

    repository.save(
        investigation,
    )

    found = repository.get(
        investigation.id,
    )

    assert found is not None
    assert found.status == investigation.status


def test_get_restores_closed_at() -> None:
    repository = SqliteInvestigationRepository(
        ":memory:",
    )

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    investigation.close()

    repository.save(
        investigation,
    )

    found = repository.get(
        investigation.id,
    )

    assert found is not None
    assert found.closed_at == investigation.closed_at


def test_list_reports_malformed_investigation_id() -> None:
    repository = SqliteInvestigationRepository(":memory:")
    repository._connection.execute(
        """
        INSERT INTO investigations (id, title, purpose, status)
        VALUES (?, ?, ?, ?)
        """,
        ("not-a-uuid", "Mars anomaly", "Find evidence", "draft"),
    )

    with pytest.raises(
        ValueError,
        match="malformed persisted investigation record: invalid id",
    ):
        repository.list()


def test_get_reports_malformed_investigation_status() -> None:
    repository = SqliteInvestigationRepository(":memory:")
    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    repository.save(investigation)
    repository._connection.execute(
        "UPDATE investigations SET status = ? WHERE id = ?",
        ("unknown", str(investigation.id.value)),
    )

    with pytest.raises(
        ValueError,
        match=(f"malformed persisted investigation {investigation.id.value}: invalid status"),
    ):
        repository.get(investigation.id)


def test_get_reports_malformed_investigation_closed_at() -> None:
    repository = SqliteInvestigationRepository(":memory:")
    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    repository.save(investigation)
    repository._connection.execute(
        "UPDATE investigations SET closed_at = ? WHERE id = ?",
        ("not-a-datetime", str(investigation.id.value)),
    )

    with pytest.raises(
        ValueError,
        match=(f"malformed persisted investigation {investigation.id.value}: invalid closed_at"),
    ):
        repository.get(investigation.id)
