import pytest

from titan.application.add_evidence import AddEvidence
from titan.application.domain_event_repository import DomainEventRepository
from titan.application.in_memory_domain_event_repository import (
    InMemoryDomainEventRepository,
)
from titan.application.in_memory_investigation_repository import (
    InMemoryInvestigationRepository,
)
from titan.application.investigation_repository import InvestigationRepository
from titan.application.unit_of_work import UnitOfWork
from titan.core.evidence import EvidenceRelationship
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


def test_add_evidence_rejects_closed_investigation() -> None:
    unit_of_work = SpyUnitOfWork()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Evaluate evidence",
    )
    investigation.pull_events()
    investigation.add_hypothesis(
        "Seasonal methane variation indicates microbial activity",
    )
    investigation.pull_events()
    hypothesis = investigation.hypotheses[0]
    investigation.close()
    investigation.pull_events()

    unit_of_work.investigations.save(
        investigation,
    )

    add_evidence = AddEvidence(
        unit_of_work,
    )

    with pytest.raises(
        ValueError,
        match="investigation is closed",
    ):
        add_evidence(
            investigation_id=investigation.id,
            hypothesis_id=hypothesis.id,
            description="Methane concentration varies seasonally",
            source="NASA Curiosity methane measurements",
            relationship=EvidenceRelationship.SUPPORTS,
        )

    assert unit_of_work.committed is False
    assert unit_of_work.rolled_back is True
    assert hypothesis.evidences == ()
