import pytest

from titan.application.confirm_hypothesis import (
    ConfirmHypothesis,
)
from titan.application.in_memory_investigation_repository import (
    InMemoryInvestigationRepository,
)
from titan.core.hypothesis import (
    Hypothesis,
    HypothesisStatus,
)
from titan.core.investigation import Investigation


def test_confirm_hypothesis_returns_confirmed_hypothesis() -> None:
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

    confirm_hypothesis = ConfirmHypothesis(
        repository,
    )

    confirmed = confirm_hypothesis(
        investigation_id=investigation.id,
        hypothesis_id=hypothesis.id,
    )

    assert confirmed is hypothesis
    assert confirmed.status is HypothesisStatus.CONFIRMED


def test_confirm_hypothesis_raises_if_investigation_not_found() -> None:
    repository = InMemoryInvestigationRepository()

    confirm_hypothesis = ConfirmHypothesis(
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
        confirm_hypothesis(
            investigation_id=investigation.id,
            hypothesis_id=hypothesis.id,
        )


def test_confirm_hypothesis_raises_if_hypothesis_not_found() -> None:
    repository = InMemoryInvestigationRepository()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    repository.save(investigation)

    unknown = Hypothesis(
        statement="Unknown hypothesis",
    )

    confirm_hypothesis = ConfirmHypothesis(
        repository,
    )

    with pytest.raises(LookupError):
        confirm_hypothesis(
            investigation_id=investigation.id,
            hypothesis_id=unknown.id,
        )
