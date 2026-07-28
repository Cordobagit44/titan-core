from titan.core.evidence import Evidence
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


def test_get_restores_hypothesis_evidences() -> None:
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
    assert found.hypotheses[0].evidences[0].description == "High-resolution orbital imagery"


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
