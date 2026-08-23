import pytest

from titan.application.create_investigation import CreateInvestigation
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
from titan.core.investigation import InvestigationCreated


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


def test_create_investigation_saves_and_returns_investigation() -> None:
    unit_of_work = SpyUnitOfWork()

    create_investigation = CreateInvestigation(
        unit_of_work,
    )

    investigation = create_investigation(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    assert investigation.title == "Mars anomaly"
    assert investigation.purpose == "Find evidence"
    assert (
        unit_of_work.investigations.get(
            investigation.id,
        )
        is investigation
    )


def test_create_investigation_persists_domain_event() -> None:
    unit_of_work = SpyUnitOfWork()

    create_investigation = CreateInvestigation(
        unit_of_work,
    )

    investigation = create_investigation(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    assert unit_of_work.domain_events.list_all() == [
        InvestigationCreated(
            investigation_id=investigation.id,
            title="Mars anomaly",
        )
    ]


def test_create_investigation_commits_unit_of_work() -> None:
    unit_of_work = SpyUnitOfWork()

    create_investigation = CreateInvestigation(
        unit_of_work,
    )

    create_investigation(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    assert unit_of_work.committed is True
    assert unit_of_work.rolled_back is False


def test_create_investigation_rolls_back_if_persistence_fails() -> None:
    unit_of_work = SpyUnitOfWork(
        domain_events=FailingDomainEventRepository(),
    )

    create_investigation = CreateInvestigation(
        unit_of_work,
    )

    with pytest.raises(
        RuntimeError,
        match="domain event persistence failed",
    ):
        create_investigation(
            title="Mars anomaly",
            purpose="Find evidence",
        )

    assert unit_of_work.committed is False
    assert unit_of_work.rolled_back is True


def test_create_investigation_rolls_back_if_purpose_is_empty() -> None:
    unit_of_work = SpyUnitOfWork()

    create_investigation = CreateInvestigation(
        unit_of_work,
    )

    with pytest.raises(
        ValueError,
        match="purpose must not be empty",
    ):
        create_investigation(
            title="Mars anomaly",
            purpose="   ",
        )

    assert unit_of_work.committed is False
    assert unit_of_work.rolled_back is True
