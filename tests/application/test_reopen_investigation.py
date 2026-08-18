import pytest

from titan.application.in_memory_domain_event_repository import (
    InMemoryDomainEventRepository,
)
from titan.application.in_memory_investigation_repository import (
    InMemoryInvestigationRepository,
)
from titan.application.reopen_investigation import (
    ReopenInvestigation,
)
from titan.core.investigation import (
    Investigation,
    InvestigationReopened,
    InvestigationStatus,
)


def test_reopen_investigation_returns_active_investigation() -> None:
    repository = InMemoryInvestigationRepository()
    event_repository = InMemoryDomainEventRepository()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    investigation.pull_events()

    investigation.activate()
    investigation.pull_events()

    investigation.close()
    investigation.pull_events()

    repository.save(
        investigation,
    )

    reopen_investigation = ReopenInvestigation(
        repository,
        event_repository,
    )

    reopened = reopen_investigation(
        investigation_id=investigation.id,
    )

    assert reopened is investigation
    assert reopened.status is InvestigationStatus.ACTIVE
    assert reopened.closed_at is None


def test_reopen_investigation_persists_domain_event() -> None:
    repository = InMemoryInvestigationRepository()
    event_repository = InMemoryDomainEventRepository()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    investigation.pull_events()

    investigation.activate()
    investigation.pull_events()

    investigation.close()
    investigation.pull_events()

    repository.save(
        investigation,
    )

    reopen_investigation = ReopenInvestigation(
        repository,
        event_repository,
    )

    reopened = reopen_investigation(
        investigation_id=investigation.id,
    )

    assert event_repository.list_all() == [
        InvestigationReopened(
            investigation_id=reopened.id,
        )
    ]


def test_reopen_investigation_raises_if_not_found() -> None:
    repository = InMemoryInvestigationRepository()
    event_repository = InMemoryDomainEventRepository()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    investigation.pull_events()

    reopen_investigation = ReopenInvestigation(
        repository,
        event_repository,
    )

    with pytest.raises(
        LookupError,
        match="investigation not found",
    ):
        reopen_investigation(
            investigation_id=investigation.id,
        )
