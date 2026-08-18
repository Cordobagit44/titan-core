import pytest

from titan.application.add_hypothesis import AddHypothesis
from titan.application.in_memory_domain_event_repository import (
    InMemoryDomainEventRepository,
)
from titan.application.in_memory_investigation_repository import (
    InMemoryInvestigationRepository,
)
from titan.core.investigation import (
    HypothesisAdded,
    Investigation,
)


def test_add_hypothesis_returns_created_hypothesis() -> None:
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

    add_hypothesis = AddHypothesis(
        repository,
        event_repository,
    )

    hypothesis = add_hypothesis(
        investigation_id=investigation.id,
        statement="Methane indicates microbial life",
    )

    assert hypothesis.statement == "Methane indicates microbial life"
    assert investigation.hypotheses[-1] is hypothesis


def test_add_hypothesis_persists_domain_event() -> None:
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

    add_hypothesis = AddHypothesis(
        repository,
        event_repository,
    )

    add_hypothesis(
        investigation_id=investigation.id,
        statement="Methane indicates microbial life",
    )

    assert event_repository.list_all() == [
        HypothesisAdded(
            investigation_id=investigation.id,
            hypothesis_statement="Methane indicates microbial life",
        )
    ]


def test_add_hypothesis_raises_if_investigation_not_found() -> None:
    repository = InMemoryInvestigationRepository()
    event_repository = InMemoryDomainEventRepository()

    add_hypothesis = AddHypothesis(
        repository,
        event_repository,
    )

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    investigation.pull_events()

    with pytest.raises(
        LookupError,
        match="investigation not found",
    ):
        add_hypothesis(
            investigation_id=investigation.id,
            statement="Methane indicates microbial life",
        )
