import pytest

from titan.core.assessment import Assessment
from titan.core.investigation import (
    Investigation,
    InvestigationId,
    InvestigationStatus,
)
from titan.core.thesis import Thesis


def test_restore_rejects_duplicate_assessment_identity() -> None:
    thesis = Thesis(statement="The anomaly is geological.")
    first = Assessment(
        thesis_id=thesis.id,
        narrative="The evidence supports the thesis with limitations.",
    )
    duplicate = Assessment(
        id=first.id,
        thesis_id=thesis.id,
        narrative="A different evaluation with the same identity.",
    )

    with pytest.raises(ValueError, match="assessment already exists"):
        Investigation.restore(
            investigation_id=InvestigationId.new(),
            title="Mars anomaly",
            purpose="Evaluate evidence",
            status=InvestigationStatus.DRAFT,
            hypotheses=(),
            theses=(thesis,),
            assessments=(first, duplicate),
        )


def test_restore_accepts_distinct_assessment_identities() -> None:
    thesis = Thesis(statement="The anomaly is geological.")
    assessments = (
        Assessment(
            thesis_id=thesis.id,
            narrative="The evidence supports the thesis with limitations.",
        ),
        Assessment(
            thesis_id=thesis.id,
            narrative="Additional evidence would improve the evaluation.",
        ),
    )

    investigation = Investigation.restore(
        investigation_id=InvestigationId.new(),
        title="Mars anomaly",
        purpose="Evaluate evidence",
        status=InvestigationStatus.DRAFT,
        hypotheses=(),
        theses=(thesis,),
        assessments=assessments,
    )

    assert investigation.assessments == assessments
    assert investigation.pull_events() == []
