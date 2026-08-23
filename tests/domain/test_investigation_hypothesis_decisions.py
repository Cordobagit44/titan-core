import pytest

from titan.core.hypothesis import HypothesisStatus
from titan.core.investigation import Investigation


def create_investigation_with_hypothesis() -> Investigation:
    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Evaluate evidence",
    )
    investigation.add_hypothesis(
        "Seasonal methane variation indicates microbial activity",
    )
    investigation.pull_events()
    return investigation


def test_investigation_confirms_hypothesis() -> None:
    investigation = create_investigation_with_hypothesis()
    hypothesis = investigation.hypotheses[0]

    target = investigation.confirm_hypothesis(
        hypothesis.id,
    )

    assert target is hypothesis
    assert hypothesis.status is HypothesisStatus.CONFIRMED


def test_investigation_rejects_hypothesis() -> None:
    investigation = create_investigation_with_hypothesis()
    hypothesis = investigation.hypotheses[0]

    target = investigation.reject_hypothesis(
        hypothesis.id,
    )

    assert target is hypothesis
    assert hypothesis.status is HypothesisStatus.REJECTED


def test_closed_investigation_rejects_hypothesis_confirmation() -> None:
    investigation = create_investigation_with_hypothesis()
    hypothesis = investigation.hypotheses[0]
    investigation.close()

    with pytest.raises(
        ValueError,
        match="investigation is closed",
    ):
        investigation.confirm_hypothesis(
            hypothesis.id,
        )

    assert hypothesis.status is HypothesisStatus.PENDING


def test_closed_investigation_rejects_hypothesis_rejection() -> None:
    investigation = create_investigation_with_hypothesis()
    hypothesis = investigation.hypotheses[0]
    investigation.close()

    with pytest.raises(
        ValueError,
        match="investigation is closed",
    ):
        investigation.reject_hypothesis(
            hypothesis.id,
        )

    assert hypothesis.status is HypothesisStatus.PENDING


def test_reopened_investigation_allows_hypothesis_confirmation() -> None:
    investigation = create_investigation_with_hypothesis()
    hypothesis = investigation.hypotheses[0]
    investigation.close()
    investigation.reopen()

    investigation.confirm_hypothesis(
        hypothesis.id,
    )

    assert hypothesis.status is HypothesisStatus.CONFIRMED


def test_reopened_investigation_allows_hypothesis_rejection() -> None:
    investigation = create_investigation_with_hypothesis()
    hypothesis = investigation.hypotheses[0]
    investigation.close()
    investigation.reopen()

    investigation.reject_hypothesis(
        hypothesis.id,
    )

    assert hypothesis.status is HypothesisStatus.REJECTED
