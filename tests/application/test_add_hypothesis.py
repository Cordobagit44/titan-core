from titan.application.add_hypothesis import AddHypothesis

from titan.application.in_memory_investigation_repository import (
    InMemoryInvestigationRepository,
)
from titan.core.investigation import Investigation


def test_add_hypothesis_returns_created_hypothesis() -> None:
    repository = InMemoryInvestigationRepository()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    repository.save(investigation)

    add_hypothesis = AddHypothesis(repository)

    hypothesis = add_hypothesis(
        investigation_id=investigation.id,
        statement="Methane indicates microbial life",
    )

    assert hypothesis.statement == ("Methane indicates microbial life")

    assert investigation.hypotheses[-1] is hypothesis


def test_add_hypothesis_raises_if_investigation_not_found() -> None:
    repository = InMemoryInvestigationRepository()

    add_hypothesis = AddHypothesis(repository)

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    try:
        add_hypothesis(
            investigation_id=investigation.id,
            statement="Methane indicates microbial life",
        )
    except LookupError:
        pass
    else:
        raise AssertionError("LookupError was not raised")
