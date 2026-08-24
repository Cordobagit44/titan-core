import pytest

from titan.core.claim import Claim
from titan.core.evidence import Evidence, EvidenceRelationship
from titan.core.hypothesis import Hypothesis
from titan.core.investigation import Investigation


def create_grounded_investigation() -> tuple[Investigation, Hypothesis, Evidence]:
    investigation = Investigation.create("Mars anomaly", "Evaluate evidence")
    investigation.add_hypothesis("Seasonal methane variation indicates microbial activity")
    hypothesis = investigation.hypotheses[0]
    evidence = Evidence(
        description="Methane concentration varies seasonally",
        source="NASA Curiosity methane measurements",
        relationship=EvidenceRelationship.SUPPORTS,
    )
    investigation.add_evidence(hypothesis.id, evidence)
    investigation.pull_events()
    hypothesis.pull_events()
    return investigation, hypothesis, evidence


def test_investigation_adds_claim_to_hypothesis() -> None:
    investigation, hypothesis, evidence = create_grounded_investigation()
    claim = Claim(statement="Methane varies seasonally", evidence_id=evidence.id)

    target = investigation.add_claim(hypothesis.id, claim)

    assert target is hypothesis
    assert hypothesis.claims == (claim,)


def test_closed_investigation_rejects_claim_attachment() -> None:
    investigation, hypothesis, evidence = create_grounded_investigation()
    investigation.close()
    investigation.pull_events()
    claim = Claim(statement="Methane varies seasonally", evidence_id=evidence.id)

    with pytest.raises(ValueError, match="investigation is closed"):
        investigation.add_claim(hypothesis.id, claim)

    assert hypothesis.claims == ()
    assert hypothesis.pull_events() == []


def test_investigation_add_claim_requires_known_hypothesis() -> None:
    investigation, _, evidence = create_grounded_investigation()
    unknown = Hypothesis(statement="Unknown hypothesis")
    claim = Claim(statement="Methane varies seasonally", evidence_id=evidence.id)

    with pytest.raises(LookupError, match="hypothesis not found"):
        investigation.add_claim(unknown.id, claim)

    assert unknown.claims == ()
    assert unknown.pull_events() == []
