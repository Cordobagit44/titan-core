from titan.application.in_memory_domain_event_repository import (
    InMemoryDomainEventRepository,
)
from titan.core.investigation import Investigation


def test_in_memory_domain_event_repository_stores_events() -> None:
    repository = InMemoryDomainEventRepository()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    events = investigation.pull_events()

    repository.save(events[0])

    assert repository.list_all() == events


def test_in_memory_domain_event_repository_preserves_multiple_events() -> None:
    repository = InMemoryDomainEventRepository()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    created_event = investigation.pull_events()[0]

    investigation.activate()
    activated_event = investigation.pull_events()[0]

    repository.save(created_event)
    repository.save(activated_event)

    assert repository.list_all() == [
        created_event,
        activated_event,
    ]
