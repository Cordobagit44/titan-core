import pytest

from titan.application.activate_investigation import ActivateInvestigation
from titan.application.in_memory_domain_event_repository import (
    InMemoryDomainEventRepository,
)
from titan.application.in_memory_investigation_repository import (
    InMemoryInvestigationRepository,
)
from titan.core.investigation import (
    Investigation,
    InvestigationActivated,
    InvestigationStatus,
)


def test_activate_investigation_activates_and_saves_investigation() -> None:
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

    activate_investigation = ActivateInvestigation(
        repository,
        event_repository,
    )

    activated = activate_investigation(
        investigation.id,
    )

    assert activated is investigation
    assert activated.status is InvestigationStatus.ACTIVE
    assert repository.get(investigation.id) is investigation


def test_activate_investigation_persists_domain_event() -> None:
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

    activate_investigation = ActivateInvestigation(
        repository,
        event_repository,
    )

    activated = activate_investigation(
        investigation.id,
    )

    assert event_repository.list_all() == [
        InvestigationActivated(
            investigation_id=activated.id,
        )
    ]


def test_activate_investigation_raises_if_not_found() -> None:
    repository = InMemoryInvestigationRepository()
    event_repository = InMemoryDomainEventRepository()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    investigation.pull_events()

    activate_investigation = ActivateInvestigation(
        repository,
        event_repository,
    )

    with pytest.raises(
        LookupError,
        match="investigation not found",
    ):
        activate_investigation(
            investigation.id,
        )
