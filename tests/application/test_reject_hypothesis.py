import pytest
from titan.application.reject_hypothesis import (
    RejectHypothesis,
)

from titan.application.in_memory_investigation_repository import (
    InMemoryInvestigationRepository,
)
from titan.core.hypothesis import (
    Hypothesis,
    HypothesisStatus,
)
from titan.core.investigation import Investigation


def test_reject_hypothesis_returns_rejected_hypothesis() -> None:
    repository = InMemoryInvestigationRepository()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    investigation.add_hypothesis(
        "Methane indicates microbial life",
    )

    repository.save(investigation)

    hypothesis = investigation.hypotheses[0]

    reject_hypothesis = RejectHypothesis(
        repository,
    )

    rejected = reject_hypothesis(
        investigation_id=investigation.id,
        hypothesis_id=hypothesis.id,
    )

    assert rejected is hypothesis
    assert rejected.status is HypothesisStatus.REJECTED


def test_reject_hypothesis_raises_if_investigation_not_found() -> None:
    repository = InMemoryInvestigationRepository()

    reject_hypothesis = RejectHypothesis(
        repository,
    )

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    investigation.add_hypothesis(
        "Methane indicates microbial life",
    )

    hypothesis = investigation.hypotheses[0]

    with pytest.raises(LookupError):
        reject_hypothesis(
            investigation_id=investigation.id,
            hypothesis_id=hypothesis.id,
        )


def test_reject_hypothesis_raises_if_hypothesis_not_found() -> None:
    repository = InMemoryInvestigationRepository()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    repository.save(investigation)

    unknown = Hypothesis(
        statement="Unknown hypothesis",
    )

    reject_hypothesis = RejectHypothesis(
        repository,
    )

    with pytest.raises(LookupError):
        reject_hypothesis(
            investigation_id=investigation.id,
            hypothesis_id=unknown.id,
        )
