from titan.core.investigation import Investigation, InvestigationStatus
from titan.core.thesis import Thesis
from titan.infrastructure.sqlite.sqlite_investigation_repository import (
    SqliteInvestigationRepository,
)


def test_save_and_get_preserves_investigation_theses() -> None:
    repository = SqliteInvestigationRepository(":memory:")
    investigation = Investigation.create("Mars anomaly", "Evaluate evidence")
    first = Thesis(statement="The anomaly is geological.")
    second = Thesis(statement="The anomaly may be artificial.")
    investigation.add_thesis(first)
    investigation.add_thesis(second)

    repository.save(investigation)
    found = repository.get(investigation.id)

    assert found is not None
    assert found.theses == (first, second)
    assert found.pull_events() == []


def test_list_preserves_investigation_theses() -> None:
    repository = SqliteInvestigationRepository(":memory:")
    investigation = Investigation.create("Mars anomaly", "Evaluate evidence")
    thesis = Thesis(statement="The anomaly is geological.")
    investigation.add_thesis(thesis)
    repository.save(investigation)

    found = repository.list()

    assert len(found) == 1
    assert found[0].theses == (thesis,)
    assert found[0].pull_events() == []


def test_resaving_replaces_prior_investigation_theses() -> None:
    repository = SqliteInvestigationRepository(":memory:")
    investigation = Investigation.create("Mars anomaly", "Evaluate evidence")
    investigation.add_thesis(Thesis(statement="Initial conclusion"))
    repository.save(investigation)
    replacement = Thesis(statement="Revised conclusion")
    restored = Investigation.restore(
        investigation_id=investigation.id,
        title=investigation.title,
        purpose=investigation.purpose,
        status=InvestigationStatus.DRAFT,
        hypotheses=(),
        theses=(replacement,),
    )

    repository.save(restored)
    found = repository.get(investigation.id)

    assert found is not None
    assert found.theses == (replacement,)
