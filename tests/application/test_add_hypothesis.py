import pytest

from titan.application.add_hypothesis import AddHypothesis
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
    HypothesisAdded,
    Investigation,
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


def test_add_hypothesis_returns_created_hypothesis() -> None:
    unit_of_work = SpyUnitOfWork()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    investigation.pull_events()

    unit_of_work.investigations.save(
        investigation,
    )

    add_hypothesis = AddHypothesis(
        unit_of_work,
    )

    hypothesis = add_hypothesis(
        investigation_id=investigation.id,
        statement="Methane indicates microbial life",
    )

    assert hypothesis.statement == "Methane indicates microbial life"
    assert investigation.hypotheses[-1] is hypothesis


def test_add_hypothesis_persists_domain_event() -> None:
    unit_of_work = SpyUnitOfWork()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    investigation.pull_events()

    unit_of_work.investigations.save(
        investigation,
    )

    add_hypothesis = AddHypothesis(
        unit_of_work,
    )

    add_hypothesis(
        investigation_id=investigation.id,
        statement="Methane indicates microbial life",
    )

    assert unit_of_work.domain_events.list_all() == [
        HypothesisAdded(
            investigation_id=investigation.id,
            hypothesis_statement="Methane indicates microbial life",
        )
    ]


def test_add_hypothesis_commits_unit_of_work() -> None:
    unit_of_work = SpyUnitOfWork()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    investigation.pull_events()

    unit_of_work.investigations.save(
        investigation,
    )

    add_hypothesis = AddHypothesis(
        unit_of_work,
    )

    add_hypothesis(
        investigation_id=investigation.id,
        statement="Methane indicates microbial life",
    )

    assert unit_of_work.committed is True
    assert unit_of_work.rolled_back is False


def test_add_hypothesis_rolls_back_if_persistence_fails() -> None:
    unit_of_work = SpyUnitOfWork(
        domain_events=FailingDomainEventRepository(),
    )

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    investigation.pull_events()

    unit_of_work.investigations.save(
        investigation,
    )

    add_hypothesis = AddHypothesis(
        unit_of_work,
    )

    with pytest.raises(
        RuntimeError,
        match="domain event persistence failed",
    ):
        add_hypothesis(
            investigation_id=investigation.id,
            statement="Methane indicates microbial life",
        )

    assert unit_of_work.committed is False
    assert unit_of_work.rolled_back is True


def test_add_hypothesis_raises_if_investigation_not_found() -> None:
    unit_of_work = SpyUnitOfWork()

    add_hypothesis = AddHypothesis(
        unit_of_work,
    )

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    investigation.pull_events()

    with pytest.raises(
        LookupError,
        match="investigation not found",
    ):
        add_hypothesis(
            investigation_id=investigation.id,
            statement="Methane indicates microbial life",
        )
