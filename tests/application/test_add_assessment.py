import pytest

from titan.application.add_assessment import AddAssessment
from titan.application.domain_event_repository import DomainEventRepository
from titan.application.in_memory_domain_event_repository import InMemoryDomainEventRepository
from titan.application.in_memory_investigation_repository import InMemoryInvestigationRepository
from titan.application.investigation_repository import InvestigationRepository
from titan.application.unit_of_work import UnitOfWork
from titan.core.investigation import AssessmentAdded, Investigation, InvestigationId
from titan.core.thesis import Thesis, ThesisId


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


def prepare_unit_of_work(
    domain_events: DomainEventRepository | None = None,
) -> tuple[SpyUnitOfWork, Investigation, Thesis]:
    unit_of_work = SpyUnitOfWork(domain_events)
    investigation = Investigation.create("Mars anomaly", "Evaluate evidence")
    thesis = Thesis(statement="The anomaly is geological.")
    investigation.add_thesis(thesis)
    investigation.pull_events()
    unit_of_work.investigations.save(investigation)
    return unit_of_work, investigation, thesis


def test_add_assessment_persists_state_event_and_commits() -> None:
    unit_of_work, investigation, thesis = prepare_unit_of_work()

    assessment = AddAssessment(unit_of_work)(
        investigation_id=investigation.id,
        thesis_id=thesis.id,
        narrative="The evidence supports the thesis with limitations.",
    )

    assert investigation.assessments == (assessment,)
    assert unit_of_work.domain_events.list_all() == [
        AssessmentAdded(investigation.id, assessment.id, thesis.id)
    ]
    assert unit_of_work.committed is True
    assert unit_of_work.rolled_back is False


def test_add_assessment_rolls_back_for_missing_investigation() -> None:
    unit_of_work = SpyUnitOfWork()

    with pytest.raises(LookupError, match="investigation not found"):
        AddAssessment(unit_of_work)(
            investigation_id=InvestigationId.new(),
            thesis_id=ThesisId.new(),
            narrative="The evidence remains incomplete.",
        )

    assert unit_of_work.committed is False
    assert unit_of_work.rolled_back is True


def test_add_assessment_rolls_back_for_unknown_thesis() -> None:
    unit_of_work, investigation, _ = prepare_unit_of_work()

    with pytest.raises(LookupError, match="thesis not found"):
        AddAssessment(unit_of_work)(
            investigation_id=investigation.id,
            thesis_id=ThesisId.new(),
            narrative="The evidence remains incomplete.",
        )

    assert investigation.assessments == ()
    assert unit_of_work.committed is False
    assert unit_of_work.rolled_back is True


def test_add_assessment_rolls_back_when_event_persistence_fails() -> None:
    unit_of_work, investigation, thesis = prepare_unit_of_work(
        FailingDomainEventRepository()
    )

    with pytest.raises(RuntimeError, match="domain event persistence failed"):
        AddAssessment(unit_of_work)(
            investigation_id=investigation.id,
            thesis_id=thesis.id,
            narrative="The evidence remains incomplete.",
        )

    assert unit_of_work.committed is False
    assert unit_of_work.rolled_back is True
