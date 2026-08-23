import pytest

from titan.application.confirm_hypothesis import ConfirmHypothesis
from titan.application.domain_event_repository import DomainEventRepository
from titan.application.in_memory_domain_event_repository import (
    InMemoryDomainEventRepository,
)
from titan.application.in_memory_investigation_repository import (
    InMemoryInvestigationRepository,
)
from titan.application.investigation_repository import InvestigationRepository
from titan.application.reject_hypothesis import RejectHypothesis
from titan.application.unit_of_work import UnitOfWork
from titan.core.hypothesis import HypothesisStatus
from titan.core.investigation import Investigation


class SpyUnitOfWork(UnitOfWork):
    def __init__(self) -> None:
        self._investigations = InMemoryInvestigationRepository()
        self._domain_events = InMemoryDomainEventRepository()
        self.committed = False
        self.rolled_back = False

    @property
    def investigations(self) -> InvestigationRepository:
        return self._investigations

    @property
    def domain_events(self) -> DomainEventRepository:
        return self._domain_events

    def commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        self.rolled_back = True


def create_closed_investigation(
    unit_of_work: SpyUnitOfWork,
) -> Investigation:
    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Evaluate evidence",
    )
    investigation.pull_events()
    investigation.add_hypothesis(
        "Seasonal methane variation indicates microbial activity",
    )
    investigation.pull_events()
    investigation.close()
    investigation.pull_events()
    unit_of_work.investigations.save(investigation)
    return investigation


def test_confirm_hypothesis_rolls_back_when_investigation_is_closed() -> None:
    unit_of_work = SpyUnitOfWork()
    investigation = create_closed_investigation(unit_of_work)
    hypothesis = investigation.hypotheses[0]

    with pytest.raises(
        ValueError,
        match="investigation is closed",
    ):
        ConfirmHypothesis(unit_of_work)(
            investigation_id=investigation.id,
            hypothesis_id=hypothesis.id,
        )

    assert hypothesis.status is HypothesisStatus.PENDING
    assert unit_of_work.domain_events.list_all() == []
    assert unit_of_work.committed is False
    assert unit_of_work.rolled_back is True


def test_reject_hypothesis_rolls_back_when_investigation_is_closed() -> None:
    unit_of_work = SpyUnitOfWork()
    investigation = create_closed_investigation(unit_of_work)
    hypothesis = investigation.hypotheses[0]

    with pytest.raises(
        ValueError,
        match="investigation is closed",
    ):
        RejectHypothesis(unit_of_work)(
            investigation_id=investigation.id,
            hypothesis_id=hypothesis.id,
        )

    assert hypothesis.status is HypothesisStatus.PENDING
    assert unit_of_work.domain_events.list_all() == []
    assert unit_of_work.committed is False
    assert unit_of_work.rolled_back is True
