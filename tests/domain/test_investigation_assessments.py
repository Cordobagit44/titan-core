import pytest

from titan.core.assessment import Assessment
from titan.core.investigation import AssessmentAdded, Investigation
from titan.core.thesis import Thesis


def create_investigation_with_thesis() -> tuple[Investigation, Thesis]:
    investigation = Investigation.create("Mars anomaly", "Evaluate evidence")
    thesis = Thesis(statement="The anomaly is geological.")
    investigation.add_thesis(thesis)
    investigation.pull_events()
    return investigation, thesis


@pytest.mark.parametrize("activate", [False, True])
def test_open_investigation_adds_assessment(activate: bool) -> None:
    investigation, thesis = create_investigation_with_thesis()
    if activate:
        investigation.activate()
        investigation.pull_events()
    assessment = Assessment(
        thesis_id=thesis.id,
        narrative="The evidence supports the thesis with important limitations.",
    )

    investigation.add_assessment(assessment)

    assert investigation.assessments == (assessment,)


def test_adding_assessment_emits_domain_event() -> None:
    investigation, thesis = create_investigation_with_thesis()
    assessment = Assessment(
        thesis_id=thesis.id,
        narrative="The evidence supports the thesis with important limitations.",
    )

    investigation.add_assessment(assessment)

    assert investigation.pull_events() == [
        AssessmentAdded(
            investigation_id=investigation.id,
            assessment_id=assessment.id,
            thesis_id=thesis.id,
        )
    ]


def test_assessment_requires_owned_thesis() -> None:
    investigation = Investigation.create("Mars anomaly", "Evaluate evidence")
    investigation.pull_events()
    assessment = Assessment(
        thesis_id=Thesis(statement="Unknown thesis").id,
        narrative="The available evidence is insufficient.",
    )

    with pytest.raises(LookupError, match="thesis not found"):
        investigation.add_assessment(assessment)

    assert investigation.assessments == ()
    assert investigation.pull_events() == []


def test_investigation_rejects_duplicate_assessment_identity() -> None:
    investigation, thesis = create_investigation_with_thesis()
    assessment = Assessment(
        thesis_id=thesis.id,
        narrative="The evidence supports the thesis with important limitations.",
    )
    investigation.add_assessment(assessment)
    investigation.pull_events()

    with pytest.raises(ValueError, match="assessment already exists"):
        investigation.add_assessment(assessment)

    assert investigation.assessments == (assessment,)
    assert investigation.pull_events() == []


def test_closed_investigation_rejects_assessment() -> None:
    investigation, thesis = create_investigation_with_thesis()
    investigation.close()
    investigation.pull_events()
    assessment = Assessment(
        thesis_id=thesis.id,
        narrative="The evidence supports the thesis with important limitations.",
    )

    with pytest.raises(ValueError, match="investigation is closed"):
        investigation.add_assessment(assessment)

    assert investigation.assessments == ()
    assert investigation.pull_events() == []


def test_equal_assessment_narratives_keep_distinct_identities() -> None:
    investigation, thesis = create_investigation_with_thesis()
    first = Assessment(
        thesis_id=thesis.id,
        narrative="The evidence remains incomplete.",
    )
    second = Assessment(
        thesis_id=thesis.id,
        narrative=first.narrative,
    )

    investigation.add_assessment(first)
    investigation.add_assessment(second)

    assert investigation.assessments == (first, second)
