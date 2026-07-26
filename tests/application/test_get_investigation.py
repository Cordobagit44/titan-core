import pytest
from titan.application.get_investigation import (
    GetInvestigation,
)

from titan.application.in_memory_investigation_repository import (
    InMemoryInvestigationRepository,
)
from titan.core.investigation import Investigation


def test_get_investigation_returns_existing_investigation() -> None:
    repository = InMemoryInvestigationRepository()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    repository.save(investigation)

    get_investigation = GetInvestigation(
        repository,
    )

    found = get_investigation(
        investigation.id,
    )

    assert found is investigation


def test_get_investigation_raises_if_not_found() -> None:
    repository = InMemoryInvestigationRepository()

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    get_investigation = GetInvestigation(
        repository,
    )

    with pytest.raises(
        LookupError,
        match="investigation not found",
    ):
        get_investigation(
            investigation.id,
        )
