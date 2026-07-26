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
