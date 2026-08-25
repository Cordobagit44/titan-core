from titan.core.assessment import Assessment
from titan.core.investigation import Investigation, InvestigationStatus
from titan.core.thesis import Thesis
from titan.infrastructure.sqlite.sqlite_investigation_repository import (
    SqliteInvestigationRepository,
)


def create_investigation_with_assessments() -> tuple[Investigation, tuple[Assessment, ...]]:
    investigation = Investigation.create("Mars anomaly", "Evaluate evidence")
    thesis = Thesis(statement="The anomaly is geological.")
    investigation.add_thesis(thesis)
    assessments = (
        Assessment(
            thesis_id=thesis.id,
            narrative="The evidence supports the thesis with limitations.",
        ),
        Assessment(
            thesis_id=thesis.id,
            narrative="Source diversity should improve before stronger reliance.",
        ),
    )
    for assessment in assessments:
        investigation.add_assessment(assessment)
    return investigation, assessments


def test_save_and_get_preserves_investigation_assessments() -> None:
    repository = SqliteInvestigationRepository(":memory:")
    investigation, assessments = create_investigation_with_assessments()

    repository.save(investigation)
    found = repository.get(investigation.id)

    assert found is not None
    assert found.assessments == assessments
    assert found.pull_events() == []


def test_list_preserves_investigation_assessments() -> None:
    repository = SqliteInvestigationRepository(":memory:")
    investigation, assessments = create_investigation_with_assessments()
    repository.save(investigation)

    found = repository.list()

    assert len(found) == 1
    assert found[0].assessments == assessments
    assert found[0].pull_events() == []


def test_resaving_replaces_prior_investigation_assessments() -> None:
    repository = SqliteInvestigationRepository(":memory:")
    investigation, _ = create_investigation_with_assessments()
    repository.save(investigation)
    thesis = investigation.theses[0]
    replacement = Assessment(
        thesis_id=thesis.id,
        narrative="The revised evaluation remains cautious.",
    )
    restored = Investigation.restore(
        investigation_id=investigation.id,
        title=investigation.title,
        purpose=investigation.purpose,
        status=InvestigationStatus.DRAFT,
        hypotheses=(),
        theses=(thesis,),
        assessments=(replacement,),
    )

    repository.save(restored)
    found = repository.get(investigation.id)

    assert found is not None
    assert found.assessments == (replacement,)
