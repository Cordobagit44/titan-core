import pytest

from titan.application.add_evidence import AddEvidence
from titan.application.in_memory_domain_event_repository import (
    InMemoryDomainEventRepository,
)
from titan.application.in_memory_investigation_repository import (
    InMemoryInvestigationRepository,
)
from titan.core.events import EvidenceAdded
from titan.core.hypothesis import Hypothesis
from titan.core.investigation import Investigation


def test_add_evidence_returns_created_evidence() -> None:
    repository = InMemoryInvestigationRepository()
    event_repository = InMemoryDomainEventRepository()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    investigation.pull_events()

    investigation.add_hypothesis(
        "Methane indicates microbial life",
    )
    investigation.pull_events()

    repository.save(
        investigation,
    )

    hypothesis = investigation.hypotheses[0]

    add_evidence = AddEvidence(
        repository,
        event_repository,
    )

    evidence = add_evidence(
        investigation_id=investigation.id,
        hypothesis_id=hypothesis.id,
        description="Methane levels vary seasonally",
    )

    assert evidence.description == "Methane levels vary seasonally"
    assert hypothesis.evidences == (evidence,)


def test_add_evidence_persists_domain_event() -> None:
    repository = InMemoryInvestigationRepository()
    event_repository = InMemoryDomainEventRepository()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    investigation.pull_events()

    investigation.add_hypothesis(
        "Methane indicates microbial life",
    )
    investigation.pull_events()

    repository.save(
        investigation,
    )

    hypothesis = investigation.hypotheses[0]

    add_evidence = AddEvidence(
        repository,
        event_repository,
    )

    evidence = add_evidence(
        investigation_id=investigation.id,
        hypothesis_id=hypothesis.id,
        description="Methane levels vary seasonally",
    )

    assert event_repository.list_all() == [
        EvidenceAdded(
            hypothesis_id=hypothesis.id,
            evidence_id=evidence.id,
        )
    ]


def test_add_evidence_raises_if_investigation_not_found() -> None:
    repository = InMemoryInvestigationRepository()
    event_repository = InMemoryDomainEventRepository()

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
        repository,
        event_repository,
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
    repository = InMemoryInvestigationRepository()
    event_repository = InMemoryDomainEventRepository()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    investigation.pull_events()

    repository.save(
        investigation,
    )

    unknown_hypothesis = Hypothesis(
        statement="Unknown hypothesis",
    )

    add_evidence = AddEvidence(
        repository,
        event_repository,
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
    repository = InMemoryInvestigationRepository()
    event_repository = InMemoryDomainEventRepository()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    investigation.pull_events()

    investigation.add_hypothesis(
        "Methane indicates microbial life",
    )
    investigation.pull_events()

    repository.save(
        investigation,
    )

    hypothesis = investigation.hypotheses[0]

    add_evidence = AddEvidence(
        repository,
        event_repository,
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
