import pytest

from titan.application.confirm_hypothesis import (
    ConfirmHypothesis,
)
from titan.application.in_memory_domain_event_repository import (
    InMemoryDomainEventRepository,
)
from titan.application.in_memory_investigation_repository import (
    InMemoryInvestigationRepository,
)
from titan.core.events import HypothesisConfirmed
from titan.core.hypothesis import (
    Hypothesis,
    HypothesisStatus,
)
from titan.core.investigation import Investigation


def test_confirm_hypothesis_returns_confirmed_hypothesis() -> None:
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

    confirm_hypothesis = ConfirmHypothesis(
        repository,
        event_repository,
    )

    confirmed = confirm_hypothesis(
        investigation_id=investigation.id,
        hypothesis_id=hypothesis.id,
    )

    assert confirmed is hypothesis
    assert confirmed.status is HypothesisStatus.CONFIRMED


def test_confirm_hypothesis_persists_domain_event() -> None:
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

    confirm_hypothesis = ConfirmHypothesis(
        repository,
        event_repository,
    )

    confirmed = confirm_hypothesis(
        investigation_id=investigation.id,
        hypothesis_id=hypothesis.id,
    )

    assert event_repository.list_all() == [
        HypothesisConfirmed(
            hypothesis_id=confirmed.id,
        )
    ]


def test_confirm_hypothesis_raises_if_investigation_not_found() -> None:
    repository = InMemoryInvestigationRepository()
    event_repository = InMemoryDomainEventRepository()

    confirm_hypothesis = ConfirmHypothesis(
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
        confirm_hypothesis(
            investigation_id=investigation.id,
            hypothesis_id=hypothesis.id,
        )


def test_confirm_hypothesis_raises_if_hypothesis_not_found() -> None:
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

    confirm_hypothesis = ConfirmHypothesis(
        repository,
        event_repository,
    )

    with pytest.raises(
        LookupError,
        match="hypothesis not found",
    ):
        confirm_hypothesis(
            investigation_id=investigation.id,
            hypothesis_id=unknown.id,
        )
