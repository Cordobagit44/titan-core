import pytest

from titan.application.close_investigation import (
    CloseInvestigation,
)
from titan.application.domain_event_repository import (
    DomainEventRepository,
)
from titan.application.in_memory_domain_event_repository import (
    InMemoryDomainEventRepository,
)
from titan.application.in_memory_investigation_repository import (
    InMemoryInvestigationRepository,
)
from titan.application.investigation_repository import (
    InvestigationRepository,
)
from titan.application.unit_of_work import UnitOfWork
from titan.core.investigation import (
    Investigation,
    InvestigationClosed,
    InvestigationStatus,
)


class SpyUnitOfWork(UnitOfWork):
    def __init__(
        self,
        domain_events: DomainEventRepository | None = None,
    ) -> None:
        self._investigations = InMemoryInvestigationRepository()
        self._domain_events = (
            domain_events if domain_events is not None else InMemoryDomainEventRepository()
        )
        self.committed = False
        self.rolled_back = False

    @property
    def investigations(
        self,
    ) -> InvestigationRepository:
        return self._investigations

    @property
    def domain_events(
        self,
    ) -> DomainEventRepository:
        return self._domain_events

    def commit(
        self,
    ) -> None:
        self.committed = True

    def rollback(
        self,
    ) -> None:
        self.rolled_back = True


class FailingDomainEventRepository(
    InMemoryDomainEventRepository,
):
    def save(
        self,
        event: object,
    ) -> None:
        raise RuntimeError(
            "domain event persistence failed",
        )


def test_close_investigation_returns_closed_investigation() -> None:
    unit_of_work = SpyUnitOfWork()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    investigation.pull_events()

    investigation.activate()
    investigation.pull_events()

    unit_of_work.investigations.save(
        investigation,
    )

    close_investigation = CloseInvestigation(
        unit_of_work,
    )

    closed = close_investigation(
        investigation_id=investigation.id,
    )

    assert closed is investigation
    assert closed.status is InvestigationStatus.CLOSED


def test_close_investigation_persists_domain_event() -> None:
    unit_of_work = SpyUnitOfWork()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    investigation.pull_events()

    investigation.activate()
    investigation.pull_events()

    unit_of_work.investigations.save(
        investigation,
    )

    close_investigation = CloseInvestigation(
        unit_of_work,
    )

    closed = close_investigation(
        investigation_id=investigation.id,
    )

    assert closed.closed_at is not None

    assert unit_of_work.domain_events.list_all() == [
        InvestigationClosed(
            investigation_id=closed.id,
            closed_at=closed.closed_at,
        )
    ]


def test_close_investigation_commits_unit_of_work() -> None:
    unit_of_work = SpyUnitOfWork()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    investigation.pull_events()

    investigation.activate()
    investigation.pull_events()

    unit_of_work.investigations.save(
        investigation,
    )

    close_investigation = CloseInvestigation(
        unit_of_work,
    )

    close_investigation(
        investigation_id=investigation.id,
    )

    assert unit_of_work.committed is True
    assert unit_of_work.rolled_back is False


def test_close_investigation_rolls_back_if_persistence_fails() -> None:
    unit_of_work = SpyUnitOfWork(
        domain_events=FailingDomainEventRepository(),
    )

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    investigation.pull_events()

    investigation.activate()
    investigation.pull_events()

    unit_of_work.investigations.save(
        investigation,
    )

    close_investigation = CloseInvestigation(
        unit_of_work,
    )

    with pytest.raises(
        RuntimeError,
        match="domain event persistence failed",
    ):
        close_investigation(
            investigation_id=investigation.id,
        )

    assert unit_of_work.committed is False
    assert unit_of_work.rolled_back is True


def test_close_investigation_raises_if_not_found() -> None:
    unit_of_work = SpyUnitOfWork()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    investigation.pull_events()

    close_investigation = CloseInvestigation(
        unit_of_work,
    )

    with pytest.raises(
        LookupError,
        match="investigation not found",
    ):
        close_investigation(
            investigation_id=investigation.id,
        )
