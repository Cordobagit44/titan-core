import pytest

from titan.application.add_thesis import AddThesis
from titan.application.domain_event_repository import DomainEventRepository
from titan.application.in_memory_domain_event_repository import (
    InMemoryDomainEventRepository,
)
from titan.application.in_memory_investigation_repository import (
    InMemoryInvestigationRepository,
)
from titan.application.investigation_repository import InvestigationRepository
from titan.application.unit_of_work import UnitOfWork
from titan.core.investigation import Investigation, InvestigationId, ThesisAdded


class SpyUnitOfWork(UnitOfWork):
    def __init__(self, domain_events: DomainEventRepository | None = None) -> None:
        self._investigations = InMemoryInvestigationRepository()
        self._domain_events = domain_events or InMemoryDomainEventRepository()
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


class FailingDomainEventRepository(InMemoryDomainEventRepository):
    def save(self, event: object) -> None:
        raise RuntimeError("domain event persistence failed")


def test_add_thesis_persists_state_event_and_commits() -> None:
    unit_of_work = SpyUnitOfWork()
    investigation = Investigation.create("Mars anomaly", "Evaluate evidence")
    investigation.pull_events()
    unit_of_work.investigations.save(investigation)

    thesis = AddThesis(unit_of_work)(
        investigation_id=investigation.id,
        statement="The anomaly is geological.",
    )

    assert investigation.theses == (thesis,)
    assert unit_of_work.domain_events.list_all() == [ThesisAdded(investigation.id, thesis.id)]
    assert unit_of_work.committed is True
    assert unit_of_work.rolled_back is False


def test_add_thesis_rolls_back_for_missing_investigation() -> None:
    unit_of_work = SpyUnitOfWork()

    with pytest.raises(LookupError, match="investigation not found"):
        AddThesis(unit_of_work)(
            investigation_id=InvestigationId.new(),
            statement="The anomaly is geological.",
        )

    assert unit_of_work.committed is False
    assert unit_of_work.rolled_back is True


def test_add_thesis_rolls_back_for_closed_investigation() -> None:
    unit_of_work = SpyUnitOfWork()
    investigation = Investigation.create("Mars anomaly", "Evaluate evidence")
    investigation.close()
    investigation.pull_events()
    unit_of_work.investigations.save(investigation)

    with pytest.raises(ValueError, match="investigation is closed"):
        AddThesis(unit_of_work)(
            investigation_id=investigation.id,
            statement="The anomaly is geological.",
        )

    assert investigation.theses == ()
    assert unit_of_work.committed is False
    assert unit_of_work.rolled_back is True


def test_add_thesis_rolls_back_when_event_persistence_fails() -> None:
    unit_of_work = SpyUnitOfWork(FailingDomainEventRepository())
    investigation = Investigation.create("Mars anomaly", "Evaluate evidence")
    investigation.pull_events()
    unit_of_work.investigations.save(investigation)

    with pytest.raises(RuntimeError, match="domain event persistence failed"):
        AddThesis(unit_of_work)(
            investigation_id=investigation.id,
            statement="The anomaly is geological.",
        )

    assert unit_of_work.committed is False
    assert unit_of_work.rolled_back is True
