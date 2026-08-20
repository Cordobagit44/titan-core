from uuid import UUID

import pytest

from titan.core.events import (
    EvidenceAdded,
    HypothesisConfirmed,
    HypothesisRejected,
)
from titan.core.evidence import Evidence
from titan.core.hypothesis import Hypothesis, HypothesisStatus


def test_create_hypothesis() -> None:
    hypothesis = Hypothesis(
        statement="NVIDIA will maintain 20% annual revenue growth.",
    )

    assert hypothesis.statement == ("NVIDIA will maintain 20% annual revenue growth.")


@pytest.mark.parametrize("invalid_statement", ["", "   "])
def test_hypothesis_rejects_empty_statement(
    invalid_statement: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="statement must not be empty",
    ):
        Hypothesis(statement=invalid_statement)


def test_hypothesis_receives_an_identifier() -> None:
    hypothesis = Hypothesis(
        statement="Credentials were compromised",
    )

    assert isinstance(hypothesis.id.value, UUID)


def test_hypotheses_receive_different_identifiers() -> None:
    first = Hypothesis(
        statement="Credentials were compromised",
    )
    second = Hypothesis(
        statement="Malware was delivered by email",
    )

    assert first.id != second.id


def test_add_evidence_to_hypothesis() -> None:
    hypothesis = Hypothesis(
        statement="Credentials were compromised",
    )
    evidence = Evidence(
        description="Firewall logs show repeated failed logins.",
    )

    hypothesis.add_evidence(evidence)

    assert hypothesis.evidences == (evidence,)


def test_add_evidence_emits_domain_event() -> None:
    hypothesis = Hypothesis(
        statement="Credentials were compromised",
    )
    evidence = Evidence(
        description="Firewall logs show repeated failed logins.",
    )

    hypothesis.add_evidence(evidence)

    events = hypothesis.pull_events()

    assert len(events) == 1
    assert isinstance(events[0], EvidenceAdded)
    assert events[0].hypothesis_id == hypothesis.id
    assert events[0].evidence_id == evidence.id


def test_hypothesis_starts_pending() -> None:
    hypothesis = Hypothesis(
        statement="Credentials were compromised",
    )

    assert hypothesis.status is HypothesisStatus.PENDING


def test_confirm_hypothesis() -> None:
    hypothesis = Hypothesis(
        statement="Credentials were compromised",
    )

    hypothesis.confirm()

    assert hypothesis.status is HypothesisStatus.CONFIRMED


def test_reject_hypothesis() -> None:
    hypothesis = Hypothesis(
        statement="Credentials were compromised",
    )

    hypothesis.reject()

    assert hypothesis.status is HypothesisStatus.REJECTED


def test_cannot_confirm_rejected_hypothesis() -> None:
    hypothesis = Hypothesis(
        statement="Credentials were compromised",
    )

    hypothesis.reject()

    with pytest.raises(
        ValueError,
        match="rejected hypothesis cannot be confirmed",
    ):
        hypothesis.confirm()


def test_cannot_reject_confirmed_hypothesis() -> None:
    hypothesis = Hypothesis(
        statement="Credentials were compromised",
    )

    hypothesis.confirm()

    with pytest.raises(
        ValueError,
        match="confirmed hypothesis cannot be rejected",
    ):
        hypothesis.reject()


def test_confirm_emits_domain_event() -> None:
    hypothesis = Hypothesis(
        statement="Credentials were compromised",
    )

    hypothesis.confirm()

    events = hypothesis.pull_events()

    assert len(events) == 1
    assert isinstance(events[0], HypothesisConfirmed)


def test_reject_emits_hypothesis_rejected_event() -> None:
    hypothesis = Hypothesis(
        statement="Credentials were compromised",
    )

    hypothesis.reject()

    events = hypothesis.pull_events()

    assert len(events) == 1
    assert isinstance(events[0], HypothesisRejected)
