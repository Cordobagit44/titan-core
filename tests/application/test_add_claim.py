import pytest

from titan.application.add_claim import AddClaim
from titan.application.domain_event_repository import DomainEventRepository
from titan.application.in_memory_domain_event_repository import (
    InMemoryDomainEventRepository,
)
from titan.application.in_memory_investigation_repository import (
    InMemoryInvestigationRepository,
)
from titan.application.investigation_repository import InvestigationRepository
from titan.application.unit_of_work import UnitOfWork
from titan.core.events import ClaimAdded
from titan.core.evidence import Evidence, EvidenceId, EvidenceRelationship
from titan.core.hypothesis import Hypothesis
from titan.core.investigation import Investigation, InvestigationId


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
) -> tuple[SpyUnitOfWork, Investigation, Evidence]:
    unit_of_work = SpyUnitOfWork(domain_events)
    investigation = Investigation.create("Mars anomaly", "Find evidence")
    investigation.pull_events()
    investigation.add_hypothesis("Methane indicates microbial activity")
    investigation.pull_events()
    hypothesis = investigation.hypotheses[0]
    evidence = Evidence(
        description="Methane varies seasonally",
        source="Mars orbiter",
        relationship=EvidenceRelationship.SUPPORTS,
    )
    investigation.add_evidence(hypothesis.id, evidence)
    hypothesis.pull_events()
    unit_of_work.investigations.save(investigation)
    return unit_of_work, investigation, evidence


def test_add_claim_persists_state_event_and_commits() -> None:
    unit_of_work, investigation, evidence = prepare_unit_of_work()
    hypothesis = investigation.hypotheses[0]

    claim = AddClaim(unit_of_work)(
        investigation_id=investigation.id,
        hypothesis_id=hypothesis.id,
        evidence_id=evidence.id,
        statement="Methane varies seasonally",
    )

    assert hypothesis.claims == (claim,)
    assert unit_of_work.domain_events.list_all() == [
        ClaimAdded(hypothesis.id, claim.id, evidence.id)
    ]
    assert unit_of_work.committed is True
    assert unit_of_work.rolled_back is False


def test_add_claim_rolls_back_for_missing_investigation() -> None:
    unit_of_work = SpyUnitOfWork()

    with pytest.raises(LookupError, match="investigation not found"):
        AddClaim(unit_of_work)(
            investigation_id=InvestigationId.new(),
            hypothesis_id=Hypothesis(statement="Unknown").id,
            evidence_id=EvidenceId.new(),
            statement="Methane varies seasonally",
        )

    assert unit_of_work.committed is False
    assert unit_of_work.rolled_back is True


def test_add_claim_rolls_back_for_unknown_evidence() -> None:
    unit_of_work, investigation, _ = prepare_unit_of_work()
    hypothesis = investigation.hypotheses[0]

    with pytest.raises(LookupError, match="claim evidence not found"):
        AddClaim(unit_of_work)(
            investigation_id=investigation.id,
            hypothesis_id=hypothesis.id,
            evidence_id=EvidenceId.new(),
            statement="Methane varies seasonally",
        )

    assert hypothesis.claims == ()
    assert unit_of_work.committed is False
    assert unit_of_work.rolled_back is True


def test_add_claim_rolls_back_when_event_persistence_fails() -> None:
    unit_of_work, investigation, evidence = prepare_unit_of_work(FailingDomainEventRepository())
    hypothesis = investigation.hypotheses[0]

    with pytest.raises(RuntimeError, match="domain event persistence failed"):
        AddClaim(unit_of_work)(
            investigation_id=investigation.id,
            hypothesis_id=hypothesis.id,
            evidence_id=evidence.id,
            statement="Methane varies seasonally",
        )

    assert unit_of_work.committed is False
    assert unit_of_work.rolled_back is True
