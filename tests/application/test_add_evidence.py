import pytest

from titan.application.add_evidence import AddEvidence
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
from titan.core.events import EvidenceAdded
from titan.core.hypothesis import Hypothesis
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


def test_add_evidence_returns_created_evidence() -> None:
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

    add_evidence = AddEvidence(
        unit_of_work,
    )

    evidence = add_evidence(
        investigation_id=investigation.id,
        hypothesis_id=hypothesis.id,
        description="Methane levels vary seasonally",
    )

    assert evidence.description == "Methane levels vary seasonally"
    assert hypothesis.evidences == (evidence,)


def test_add_evidence_persists_domain_event() -> None:
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

    add_evidence = AddEvidence(
        unit_of_work,
    )

    evidence = add_evidence(
        investigation_id=investigation.id,
        hypothesis_id=hypothesis.id,
        description="Methane levels vary seasonally",
    )

    assert unit_of_work.domain_events.list_all() == [
        EvidenceAdded(
            hypothesis_id=hypothesis.id,
            evidence_id=evidence.id,
        )
    ]


def test_add_evidence_commits_unit_of_work() -> None:
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

    add_evidence = AddEvidence(
        unit_of_work,
    )

    add_evidence(
        investigation_id=investigation.id,
        hypothesis_id=hypothesis.id,
        description="Methane levels vary seasonally",
    )

    assert unit_of_work.committed is True
    assert unit_of_work.rolled_back is False


def test_add_evidence_rolls_back_if_persistence_fails() -> None:
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

    add_evidence = AddEvidence(
        unit_of_work,
    )

    with pytest.raises(
        RuntimeError,
        match="domain event persistence failed",
    ):
        add_evidence(
            investigation_id=investigation.id,
            hypothesis_id=hypothesis.id,
            description="Methane levels vary seasonally",
        )

    assert unit_of_work.committed is False
    assert unit_of_work.rolled_back is True


def test_add_evidence_raises_if_investigation_not_found() -> None:
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

    add_evidence = AddEvidence(
        unit_of_work,
    )

    with pytest.raises(
        LookupError,
        match="investigation not found",
    ):
        add_evidence(
            investigation_id=investigation.id,
            hypothesis_id=hypothesis.id,
            description="Methane levels vary seasonally",
        )


def test_add_evidence_raises_if_hypothesis_not_found() -> None:
    unit_of_work = SpyUnitOfWork()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    investigation.pull_events()

    unit_of_work.investigations.save(
        investigation,
    )

    unknown_hypothesis = Hypothesis(
        statement="Unknown hypothesis",
    )

    add_evidence = AddEvidence(
        unit_of_work,
    )

    with pytest.raises(
        LookupError,
        match="hypothesis not found",
    ):
        add_evidence(
            investigation_id=investigation.id,
            hypothesis_id=unknown_hypothesis.id,
            description="Methane levels vary seasonally",
        )


def test_add_evidence_validates_description() -> None:
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

    add_evidence = AddEvidence(
        unit_of_work,
    )

    with pytest.raises(
        ValueError,
        match="description must not be empty",
    ):
        add_evidence(
            investigation_id=investigation.id,
            hypothesis_id=hypothesis.id,
            description="   ",
        )
