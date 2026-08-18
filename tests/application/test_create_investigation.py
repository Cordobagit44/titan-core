from titan.application.create_investigation import CreateInvestigation
from titan.application.in_memory_domain_event_repository import (
    InMemoryDomainEventRepository,
)
from titan.application.in_memory_investigation_repository import (
    InMemoryInvestigationRepository,
)
from titan.core.investigation import InvestigationCreated


def test_create_investigation_saves_and_returns_investigation() -> None:
    repository = InMemoryInvestigationRepository()
    event_repository = InMemoryDomainEventRepository()

    create_investigation = CreateInvestigation(
        repository,
        event_repository,
    )

    investigation = create_investigation(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    assert investigation.title == "Mars anomaly"
    assert investigation.purpose == "Find evidence"
    assert repository.get(investigation.id) is investigation


def test_create_investigation_persists_domain_event() -> None:
    repository = InMemoryInvestigationRepository()
    event_repository = InMemoryDomainEventRepository()

    create_investigation = CreateInvestigation(
        repository,
        event_repository,
    )

    investigation = create_investigation(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    assert event_repository.list_all() == [
        InvestigationCreated(
            investigation_id=investigation.id,
            title="Mars anomaly",
        )
    ]
