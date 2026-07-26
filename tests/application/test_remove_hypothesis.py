import pytest

from titan.application.in_memory_investigation_repository import (
    InMemoryInvestigationRepository,
)
from titan.application.remove_hypothesis import (
    RemoveHypothesis,
)
from titan.core.hypothesis import HypothesisId
from titan.core.investigation import Investigation


def test_remove_hypothesis_removes_existing_hypothesis() -> None:
    repository = InMemoryInvestigationRepository()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    investigation.add_hypothesis(
        statement="The signal is artificial",
    )

    hypothesis = investigation.hypotheses[0]
    repository.save(investigation)

    remove_hypothesis = RemoveHypothesis(
        repository,
    )

    remove_hypothesis(
        investigation.id,
        hypothesis.id,
    )

    assert investigation.hypotheses == ()


def test_remove_hypothesis_raises_if_investigation_not_found() -> None:
    repository = InMemoryInvestigationRepository()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    remove_hypothesis = RemoveHypothesis(
        repository,
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
    repository = InMemoryInvestigationRepository()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    repository.save(investigation)

    remove_hypothesis = RemoveHypothesis(
        repository,
    )

    with pytest.raises(
        LookupError,
        match="hypothesis not found",
    ):
        remove_hypothesis(
            investigation.id,
            HypothesisId.new(),
        )
