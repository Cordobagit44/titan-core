from titan.application.in_memory_domain_event_repository import (
    InMemoryDomainEventRepository,
)
from titan.application.persist_domain_events import persist_domain_events
from titan.core.investigation import (
    Investigation,
    InvestigationCreated,
)


def test_persist_domain_events_saves_all_pending_events() -> None:
    event_repository = InMemoryDomainEventRepository()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    persist_domain_events(
        investigation,
        event_repository,
    )

    assert event_repository.list_all() == [
        InvestigationCreated(
            investigation_id=investigation.id,
            title="Mars anomaly",
        )
    ]


def test_persist_domain_events_clears_persisted_events() -> None:
    event_repository = InMemoryDomainEventRepository()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    persist_domain_events(
        investigation,
        event_repository,
    )

    assert investigation.pull_events() == []
