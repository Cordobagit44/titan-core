import pytest

from titan.core.hypothesis import HypothesisId
from titan.core.investigation import (
    HypothesisRemoved,
    Investigation,
)


def test_remove_hypothesis_removes_existing_hypothesis() -> None:
    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    investigation.add_hypothesis(
        statement="The signal is artificial",
    )

    hypothesis = investigation.hypotheses[0]

    investigation.remove_hypothesis(
        hypothesis.id,
    )

    assert investigation.hypotheses == ()


def test_remove_hypothesis_records_event() -> None:
    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    investigation.add_hypothesis(
        statement="The signal is artificial",
    )

    hypothesis = investigation.hypotheses[0]

    investigation.pull_events()

    investigation.remove_hypothesis(
        hypothesis.id,
    )

    events = investigation.pull_events()

    assert events == [
        HypothesisRemoved(
            investigation_id=investigation.id,
            hypothesis_id=hypothesis.id,
        ),
    ]


def test_remove_hypothesis_raises_if_not_found() -> None:
    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )

    with pytest.raises(
        LookupError,
        match="hypothesis not found",
    ):
        investigation.remove_hypothesis(
            HypothesisId.new(),
        )
