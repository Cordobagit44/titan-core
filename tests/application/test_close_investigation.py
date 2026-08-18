import pytest

from titan.application.close_investigation import (
    CloseInvestigation,
)
from titan.application.in_memory_domain_event_repository import (
    InMemoryDomainEventRepository,
)
from titan.application.in_memory_investigation_repository import (
    InMemoryInvestigationRepository,
)
from titan.core.investigation import (
    Investigation,
    InvestigationClosed,
    InvestigationStatus,
)


def test_close_investigation_returns_closed_investigation() -> None:
    repository = InMemoryInvestigationRepository()
    event_repository = InMemoryDomainEventRepository()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    investigation.pull_events()

    investigation.activate()
    investigation.pull_events()

    repository.save(
        investigation,
    )

    close_investigation = CloseInvestigation(
        repository,
        event_repository,
    )

    closed = close_investigation(
        investigation_id=investigation.id,
    )

    assert closed is investigation
    assert closed.status is InvestigationStatus.CLOSED


def test_close_investigation_persists_domain_event() -> None:
    repository = InMemoryInvestigationRepository()
    event_repository = InMemoryDomainEventRepository()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    investigation.pull_events()

    investigation.activate()
    investigation.pull_events()

    repository.save(
        investigation,
    )

    close_investigation = CloseInvestigation(
        repository,
        event_repository,
    )

    closed = close_investigation(
        investigation_id=investigation.id,
    )

    assert closed.closed_at is not None

    assert event_repository.list_all() == [
        InvestigationClosed(
            investigation_id=closed.id,
            closed_at=closed.closed_at,
        )
    ]


def test_close_investigation_raises_if_not_found() -> None:
    repository = InMemoryInvestigationRepository()
    event_repository = InMemoryDomainEventRepository()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    investigation.pull_events()

    close_investigation = CloseInvestigation(
        repository,
        event_repository,
    )

    with pytest.raises(
        LookupError,
        match="investigation not found",
    ):
        close_investigation(
            investigation_id=investigation.id,
        )
