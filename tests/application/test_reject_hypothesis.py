import pytest

from titan.application.in_memory_domain_event_repository import (
    InMemoryDomainEventRepository,
)
from titan.application.in_memory_investigation_repository import (
    InMemoryInvestigationRepository,
)
from titan.application.reject_hypothesis import (
    RejectHypothesis,
)
from titan.core.events import HypothesisRejected
from titan.core.hypothesis import (
    Hypothesis,
    HypothesisStatus,
)
from titan.core.investigation import Investigation


def test_reject_hypothesis_returns_rejected_hypothesis() -> None:
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

    reject_hypothesis = RejectHypothesis(
        repository,
        event_repository,
    )

    rejected = reject_hypothesis(
        investigation_id=investigation.id,
        hypothesis_id=hypothesis.id,
    )

    assert rejected is hypothesis
    assert rejected.status is HypothesisStatus.REJECTED


def test_reject_hypothesis_persists_domain_event() -> None:
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

    reject_hypothesis = RejectHypothesis(
        repository,
        event_repository,
    )

    rejected = reject_hypothesis(
        investigation_id=investigation.id,
        hypothesis_id=hypothesis.id,
    )

    assert event_repository.list_all() == [
        HypothesisRejected(
            hypothesis_id=rejected.id,
        )
    ]


def test_reject_hypothesis_raises_if_investigation_not_found() -> None:
    repository = InMemoryInvestigationRepository()
    event_repository = InMemoryDomainEventRepository()

    reject_hypothesis = RejectHypothesis(
        repository,
        event_repository,
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
        reject_hypothesis(
            investigation_id=investigation.id,
            hypothesis_id=hypothesis.id,
        )


def test_reject_hypothesis_raises_if_hypothesis_not_found() -> None:
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

    unknown = Hypothesis(
        statement="Unknown hypothesis",
    )

    reject_hypothesis = RejectHypothesis(
        repository,
        event_repository,
    )

    with pytest.raises(
        LookupError,
        match="hypothesis not found",
    ):
        reject_hypothesis(
            investigation_id=investigation.id,
            hypothesis_id=unknown.id,
        )
