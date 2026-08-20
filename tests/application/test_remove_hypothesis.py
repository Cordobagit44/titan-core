import pytest

from titan.application.in_memory_domain_event_repository import (
    InMemoryDomainEventRepository,
)
from titan.application.in_memory_investigation_repository import (
    InMemoryInvestigationRepository,
)
from titan.application.remove_hypothesis import (
    RemoveHypothesis,
)
from titan.core.hypothesis import HypothesisId
from titan.core.investigation import (
    HypothesisRemoved,
    Investigation,
)


def test_remove_hypothesis_removes_existing_hypothesis() -> None:
    repository = InMemoryInvestigationRepository()
    event_repository = InMemoryDomainEventRepository()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    investigation.pull_events()

    investigation.add_hypothesis(
        statement="The signal is artificial",
    )
    investigation.pull_events()

    hypothesis = investigation.hypotheses[0]

    repository.save(
        investigation,
    )

    remove_hypothesis = RemoveHypothesis(
        repository,
        event_repository,
    )

    remove_hypothesis(
        investigation.id,
        hypothesis.id,
    )

    assert investigation.hypotheses == ()


def test_remove_hypothesis_persists_domain_event() -> None:
    repository = InMemoryInvestigationRepository()
    event_repository = InMemoryDomainEventRepository()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    investigation.pull_events()

    investigation.add_hypothesis(
        statement="The signal is artificial",
    )
    investigation.pull_events()

    hypothesis = investigation.hypotheses[0]

    repository.save(
        investigation,
    )

    remove_hypothesis = RemoveHypothesis(
        repository,
        event_repository,
    )

    remove_hypothesis(
        investigation.id,
        hypothesis.id,
    )

    assert event_repository.list_all() == [
        HypothesisRemoved(
            investigation_id=investigation.id,
            hypothesis_id=hypothesis.id,
        )
    ]


def test_remove_hypothesis_raises_if_investigation_not_found() -> None:
    repository = InMemoryInvestigationRepository()
    event_repository = InMemoryDomainEventRepository()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    investigation.pull_events()

    remove_hypothesis = RemoveHypothesis(
        repository,
        event_repository,
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
    event_repository = InMemoryDomainEventRepository()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    investigation.pull_events()

    repository.save(
        investigation,
    )

    remove_hypothesis = RemoveHypothesis(
        repository,
        event_repository,
    )

    with pytest.raises(
        LookupError,
        match="hypothesis not found",
    ):
        remove_hypothesis(
            investigation.id,
            HypothesisId.new(),
        )
