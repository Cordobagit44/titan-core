import pytest

from titan.core.evidence import Evidence, EvidenceRelationship
from titan.core.hypothesis import Hypothesis
from titan.core.investigation import Investigation


def create_evidence() -> Evidence:
    return Evidence(
        description="Methane concentration varies seasonally",
        source="NASA Curiosity methane measurements",
        relationship=EvidenceRelationship.SUPPORTS,
    )


def test_investigation_adds_evidence_to_hypothesis() -> None:
    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Evaluate evidence",
    )
    investigation.add_hypothesis(
        "Seasonal methane variation indicates microbial activity",
    )
    hypothesis = investigation.hypotheses[0]
    evidence = create_evidence()

    target = investigation.add_evidence(
        hypothesis_id=hypothesis.id,
        evidence=evidence,
    )

    assert target is hypothesis
    assert hypothesis.evidences == (evidence,)


def test_investigation_rejects_evidence_when_closed() -> None:
    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Evaluate evidence",
    )
    investigation.add_hypothesis(
        "Seasonal methane variation indicates microbial activity",
    )
    hypothesis = investigation.hypotheses[0]
    investigation.close()

    with pytest.raises(
        ValueError,
        match="investigation is closed",
    ):
        investigation.add_evidence(
            hypothesis_id=hypothesis.id,
            evidence=create_evidence(),
        )

    assert hypothesis.evidences == ()


def test_investigation_add_evidence_requires_known_hypothesis() -> None:
    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Evaluate evidence",
    )
    unknown_hypothesis = Hypothesis(
        statement="Unknown hypothesis",
    )

    with pytest.raises(
        LookupError,
        match="hypothesis not found",
    ):
        investigation.add_evidence(
            hypothesis_id=unknown_hypothesis.id,
            evidence=create_evidence(),
        )
