import pytest

from titan.application.confirm_hypothesis import (
    ConfirmHypothesis,
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
from titan.core.events import HypothesisConfirmed
from titan.core.hypothesis import (
    Hypothesis,
    HypothesisStatus,
)
from titan.core.investigation import Investigation


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


def test_confirm_hypothesis_returns_confirmed_hypothesis() -> None:
    unit_of_work = SpyUnitOfWork()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    investigation.pull_events()

    investigation.add_hypothesis(
        "Methane indicates microbial life",
    )
    investigation.pull_events()

    unit_of_work.investigations.save(
        investigation,
    )

    hypothesis = investigation.hypotheses[0]

    confirm_hypothesis = ConfirmHypothesis(
        unit_of_work,
    )

    confirmed = confirm_hypothesis(
        investigation_id=investigation.id,
        hypothesis_id=hypothesis.id,
    )

    assert confirmed is hypothesis
    assert confirmed.status is HypothesisStatus.CONFIRMED


def test_confirm_hypothesis_persists_domain_event() -> None:
    unit_of_work = SpyUnitOfWork()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    investigation.pull_events()

    investigation.add_hypothesis(
        "Methane indicates microbial life",
    )
    investigation.pull_events()

    unit_of_work.investigations.save(
        investigation,
    )

    hypothesis = investigation.hypotheses[0]

    confirm_hypothesis = ConfirmHypothesis(
        unit_of_work,
    )

    confirmed = confirm_hypothesis(
        investigation_id=investigation.id,
        hypothesis_id=hypothesis.id,
    )

    assert unit_of_work.domain_events.list_all() == [
        HypothesisConfirmed(
            hypothesis_id=confirmed.id,
        )
    ]


def test_confirm_hypothesis_commits_unit_of_work() -> None:
    unit_of_work = SpyUnitOfWork()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    investigation.pull_events()

    investigation.add_hypothesis(
        "Methane indicates microbial life",
    )
    investigation.pull_events()

    unit_of_work.investigations.save(
        investigation,
    )

    hypothesis = investigation.hypotheses[0]

    confirm_hypothesis = ConfirmHypothesis(
        unit_of_work,
    )

    confirm_hypothesis(
        investigation_id=investigation.id,
        hypothesis_id=hypothesis.id,
    )

    assert unit_of_work.committed is True
    assert unit_of_work.rolled_back is False


def test_confirm_hypothesis_rolls_back_if_persistence_fails() -> None:
    unit_of_work = SpyUnitOfWork(
        domain_events=FailingDomainEventRepository(),
    )

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    investigation.pull_events()

    investigation.add_hypothesis(
        "Methane indicates microbial life",
    )
    investigation.pull_events()

    unit_of_work.investigations.save(
        investigation,
    )

    hypothesis = investigation.hypotheses[0]

    confirm_hypothesis = ConfirmHypothesis(
        unit_of_work,
    )

    with pytest.raises(
        RuntimeError,
        match="domain event persistence failed",
    ):
        confirm_hypothesis(
            investigation_id=investigation.id,
            hypothesis_id=hypothesis.id,
        )

    assert unit_of_work.committed is False
    assert unit_of_work.rolled_back is True


def test_confirm_hypothesis_rolls_back_if_already_confirmed() -> None:
    unit_of_work = SpyUnitOfWork()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    investigation.pull_events()
    investigation.add_hypothesis(
        "Methane indicates microbial life",
    )
    investigation.pull_events()

    hypothesis = investigation.hypotheses[0]
    hypothesis.confirm()
    hypothesis.pull_events()
    unit_of_work.investigations.save(investigation)

    confirm_hypothesis = ConfirmHypothesis(unit_of_work)

    with pytest.raises(
        ValueError,
        match="hypothesis is already confirmed",
    ):
        confirm_hypothesis(
            investigation_id=investigation.id,
            hypothesis_id=hypothesis.id,
        )

    assert unit_of_work.committed is False
    assert unit_of_work.rolled_back is True
    assert unit_of_work.domain_events.list_all() == []


def test_confirm_hypothesis_raises_if_investigation_not_found() -> None:
    unit_of_work = SpyUnitOfWork()

    confirm_hypothesis = ConfirmHypothesis(
        unit_of_work,
    )

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    investigation.pull_events()

    investigation.add_hypothesis(
        "Methane indicates microbial life",
    )
    investigation.pull_events()

    hypothesis = investigation.hypotheses[0]

    with pytest.raises(
        LookupError,
        match="investigation not found",
    ):
        confirm_hypothesis(
            investigation_id=investigation.id,
            hypothesis_id=hypothesis.id,
        )


def test_confirm_hypothesis_raises_if_hypothesis_not_found() -> None:
    unit_of_work = SpyUnitOfWork()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    investigation.pull_events()

    unit_of_work.investigations.save(
        investigation,
    )

    unknown = Hypothesis(
        statement="Unknown hypothesis",
    )

    confirm_hypothesis = ConfirmHypothesis(
        unit_of_work,
    )

    with pytest.raises(
        LookupError,
        match="hypothesis not found",
    ):
        confirm_hypothesis(
            investigation_id=investigation.id,
            hypothesis_id=unknown.id,
        )
