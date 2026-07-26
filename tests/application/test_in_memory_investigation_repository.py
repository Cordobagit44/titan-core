from titan.application.in_memory_investigation_repository import (
    InMemoryInvestigationRepository,
)
from titan.core.investigation import Investigation


def test_saved_investigation_can_be_retrieved() -> None:
    repository = InMemoryInvestigationRepository()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    repository.save(investigation)

    loaded = repository.get(investigation.id)

    assert loaded is investigation


def test_unknown_investigation_returns_none() -> None:
    repository = InMemoryInvestigationRepository()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    assert repository.get(investigation.id) is None
