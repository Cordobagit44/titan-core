from titan.application.create_investigation import CreateInvestigation
from titan.application.in_memory_investigation_repository import (
    InMemoryInvestigationRepository,
)


def test_create_investigation_saves_and_returns_investigation() -> None:
    repository = InMemoryInvestigationRepository()
    create_investigation = CreateInvestigation(repository)

    investigation = create_investigation(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    assert investigation.title == "Mars anomaly"
    assert investigation.purpose == "Find evidence"
    assert repository.get(investigation.id) is investigation
