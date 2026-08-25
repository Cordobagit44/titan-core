from datetime import UTC, datetime, timedelta

import pytest

from titan.core.assessment import Assessment
from titan.core.investigation import Investigation
from titan.core.thesis import Thesis, ThesisId


def create_investigation_with_thesis() -> tuple[Investigation, Thesis]:
    investigation = Investigation.create("Mars anomaly", "Evaluate evidence")
    thesis = Thesis(statement="The anomaly is geological.")
    investigation.add_thesis(thesis)
    investigation.pull_events()
    return investigation, thesis


def test_latest_assessment_for_returns_most_recent_timestamp() -> None:
    investigation, thesis = create_investigation_with_thesis()
    later = datetime(2026, 8, 25, 13, 0, tzinfo=UTC)
    earlier = later - timedelta(hours=1)
    first = Assessment(
        thesis_id=thesis.id,
        narrative="The evidence is initially limited.",
        recorded_at=earlier,
    )
    latest = Assessment(
        thesis_id=thesis.id,
        narrative="New evidence strengthens the thesis.",
        recorded_at=later,
    )
    investigation.add_assessment(latest)
    investigation.add_assessment(first)
    investigation.pull_events()

    assert investigation.latest_assessment_for(thesis.id) is latest
    assert investigation.pull_events() == []


def test_latest_assessment_for_returns_none_without_assessments() -> None:
    investigation, thesis = create_investigation_with_thesis()

    assert investigation.latest_assessment_for(thesis.id) is None
    assert investigation.pull_events() == []


def test_latest_assessment_for_rejects_unknown_thesis() -> None:
    investigation, _ = create_investigation_with_thesis()

    with pytest.raises(LookupError, match="thesis not found"):
        investigation.latest_assessment_for(ThesisId.new())

    assert investigation.pull_events() == []


def test_latest_assessment_for_uses_latest_attachment_when_timestamps_match() -> None:
    investigation, thesis = create_investigation_with_thesis()
    recorded_at = datetime(2026, 8, 25, 13, 0, tzinfo=UTC)
    first = Assessment(
        thesis_id=thesis.id,
        narrative="First evaluation.",
        recorded_at=recorded_at,
    )
    second = Assessment(
        thesis_id=thesis.id,
        narrative="Second evaluation.",
        recorded_at=recorded_at,
    )
    investigation.add_assessment(first)
    investigation.add_assessment(second)
    investigation.pull_events()

    assert investigation.latest_assessment_for(thesis.id) is second
    assert investigation.pull_events() == []


def test_closed_investigation_allows_latest_assessment_lookup() -> None:
    investigation, thesis = create_investigation_with_thesis()
    assessment = Assessment(
        thesis_id=thesis.id,
        narrative="The thesis remains plausible.",
    )
    investigation.add_assessment(assessment)
    investigation.close()
    investigation.pull_events()

    assert investigation.latest_assessment_for(thesis.id) is assessment
    assert investigation.pull_events() == []
