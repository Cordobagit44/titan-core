import pytest

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
from titan.application.remove_hypothesis import (
    RemoveHypothesis,
)
from titan.application.unit_of_work import UnitOfWork
from titan.core.hypothesis import HypothesisId, HypothesisStatus
from titan.core.investigation import (
    HypothesisRemoved,
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


def test_remove_hypothesis_removes_existing_hypothesis() -> None:
    unit_of_work = SpyUnitOfWork()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    investigation.pull_events()

    investigation.add_hypothesis(
        statement="The signal is artificial",
    )
    investigation.pull_events()

    hypothesis = investigation.hypotheses[0]

    unit_of_work.investigations.save(
        investigation,
    )

    remove_hypothesis = RemoveHypothesis(
        unit_of_work,
    )

    remove_hypothesis(
        investigation.id,
        hypothesis.id,
    )

    assert investigation.hypotheses == ()


def test_remove_hypothesis_persists_domain_event() -> None:
    unit_of_work = SpyUnitOfWork()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    investigation.pull_events()

    investigation.add_hypothesis(
        statement="The signal is artificial",
    )
    investigation.pull_events()

    hypothesis = investigation.hypotheses[0]

    unit_of_work.investigations.save(
        investigation,
    )

    remove_hypothesis = RemoveHypothesis(
        unit_of_work,
    )

    remove_hypothesis(
        investigation.id,
        hypothesis.id,
    )

    assert unit_of_work.domain_events.list_all() == [
        HypothesisRemoved(
            investigation_id=investigation.id,
            hypothesis_id=hypothesis.id,
        )
    ]


def test_remove_hypothesis_commits_unit_of_work() -> None:
    unit_of_work = SpyUnitOfWork()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    investigation.pull_events()

    investigation.add_hypothesis(
        statement="The signal is artificial",
    )
    investigation.pull_events()

    hypothesis = investigation.hypotheses[0]

    unit_of_work.investigations.save(
        investigation,
    )

    remove_hypothesis = RemoveHypothesis(
        unit_of_work,
    )

    remove_hypothesis(
        investigation.id,
        hypothesis.id,
    )

    assert unit_of_work.committed is True
    assert unit_of_work.rolled_back is False


def test_remove_hypothesis_rolls_back_if_persistence_fails() -> None:
    unit_of_work = SpyUnitOfWork(
        domain_events=FailingDomainEventRepository(),
    )

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    investigation.pull_events()

    investigation.add_hypothesis(
        statement="The signal is artificial",
    )
    investigation.pull_events()

    hypothesis = investigation.hypotheses[0]

    unit_of_work.investigations.save(
        investigation,
    )

    remove_hypothesis = RemoveHypothesis(
        unit_of_work,
    )

    with pytest.raises(
        RuntimeError,
        match="domain event persistence failed",
    ):
        remove_hypothesis(
            investigation.id,
            hypothesis.id,
        )

    assert unit_of_work.committed is False
    assert unit_of_work.rolled_back is True


def test_remove_hypothesis_raises_if_investigation_not_found() -> None:
    unit_of_work = SpyUnitOfWork()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    investigation.pull_events()

    remove_hypothesis = RemoveHypothesis(
        unit_of_work,
    )

    with pytest.raises(
        LookupError,
        match="investigation not found",
    ):
        remove_hypothesis(
            investigation.id,
            HypothesisId.new(),
        )


def test_remove_hypothesis_raises_if_hypothesis_not_found() -> None:
    unit_of_work = SpyUnitOfWork()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    investigation.pull_events()

    unit_of_work.investigations.save(
        investigation,
    )

    remove_hypothesis = RemoveHypothesis(
        unit_of_work,
    )

    with pytest.raises(
        LookupError,
        match="hypothesis not found",
    ):
        remove_hypothesis(
            investigation.id,
            HypothesisId.new(),
        )


@pytest.mark.parametrize(
    "status",
    [HypothesisStatus.CONFIRMED, HypothesisStatus.REJECTED],
)
def test_remove_hypothesis_rolls_back_if_hypothesis_is_decided(
    status: HypothesisStatus,
) -> None:
    unit_of_work = SpyUnitOfWork()
    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    investigation.pull_events()
    investigation.add_hypothesis(
        statement="The signal is artificial",
    )
    investigation.pull_events()
    hypothesis = investigation.hypotheses[0]

    if status is HypothesisStatus.CONFIRMED:
        hypothesis.confirm()
    else:
        hypothesis.reject()
    hypothesis.pull_events()

    unit_of_work.investigations.save(investigation)

    with pytest.raises(
        ValueError,
        match="decided hypothesis cannot be removed",
    ):
        RemoveHypothesis(unit_of_work)(
            investigation.id,
            hypothesis.id,
        )

    assert investigation.hypotheses == (hypothesis,)
    assert unit_of_work.domain_events.list_all() == []
    assert unit_of_work.committed is False
    assert unit_of_work.rolled_back is True
