from titan.application.in_memory_investigation_repository import (
    InMemoryInvestigationRepository,
)
from titan.application.list_investigations import (
    ListInvestigations,
)
from titan.core.investigation import Investigation


def test_list_investigations_returns_empty_tuple() -> None:
    repository = InMemoryInvestigationRepository()

    list_investigations = ListInvestigations(
        repository,
    )

    investigations = list_investigations()

    assert investigations == ()


def test_list_investigations_returns_saved_investigations() -> None:
    repository = InMemoryInvestigationRepository()

    first = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    second = Investigation.create(
        title="Europa ocean",
        purpose="Search biosignatures",
    )

    repository.save(first)
    repository.save(second)

    list_investigations = ListInvestigations(
        repository,
    )

    investigations = list_investigations()

    assert investigations == (
        first,
        second,
    )
