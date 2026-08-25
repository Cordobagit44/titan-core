from uuid import uuid4

import pytest

from titan.core.assessment import Assessment, AssessmentId
from titan.core.thesis import ThesisId


def test_assessment_has_generated_identity_and_thesis_reference() -> None:
    thesis_id = ThesisId.new()

    assessment = Assessment(
        thesis_id=thesis_id,
        narrative="Evidence supports the thesis, but source diversity remains limited.",
    )

    assert isinstance(assessment.id, AssessmentId)
    assert assessment.thesis_id == thesis_id


@pytest.mark.parametrize("invalid_narrative", ["", "   "])
def test_assessment_rejects_blank_narrative(invalid_narrative: str) -> None:
    with pytest.raises(ValueError, match="narrative must not be empty"):
        Assessment(
            thesis_id=ThesisId.new(),
            narrative=invalid_narrative,
        )


def test_assessment_supports_explicit_identity_reconstruction() -> None:
    assessment_id = AssessmentId(value=uuid4())

    assessment = Assessment(
        id=assessment_id,
        thesis_id=ThesisId.new(),
        narrative="The thesis is plausible but remains provisional.",
    )

    assert assessment.id == assessment_id


def test_equal_assessment_narratives_keep_distinct_identities() -> None:
    thesis_id = ThesisId.new()
    first = Assessment(
        thesis_id=thesis_id,
        narrative="The thesis is plausible but remains provisional.",
    )
    second = Assessment(
        thesis_id=thesis_id,
        narrative=first.narrative,
    )

    assert first.id != second.id
