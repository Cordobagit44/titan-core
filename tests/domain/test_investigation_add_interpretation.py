import pytest

from titan.core.claim import Claim
from titan.core.evidence import Evidence, EvidenceRelationship
from titan.core.hypothesis import Hypothesis
from titan.core.interpretation import Interpretation
from titan.core.investigation import Investigation


def create_reasoning_chain() -> tuple[Investigation, Hypothesis, Claim]:
    investigation = Investigation.create("Mars anomaly", "Evaluate evidence")
    investigation.add_hypothesis("Methane indicates microbial activity")
    hypothesis = investigation.hypotheses[0]
    evidence = Evidence(
        description="Methane varies seasonally",
        source="Mars orbiter",
        relationship=EvidenceRelationship.SUPPORTS,
    )
    investigation.add_evidence(hypothesis.id, evidence)
    claim = Claim(statement="Methane varies seasonally", evidence_id=evidence.id)
    investigation.add_claim(hypothesis.id, claim)
    investigation.pull_events()
    hypothesis.pull_events()
    return investigation, hypothesis, claim


def create_interpretation(hypothesis: Hypothesis, claim: Claim) -> Interpretation:
    return Interpretation(
        hypothesis_id=hypothesis.id,
        claim_id=claim.id,
        rationale="Seasonal variation is consistent with a biological cycle.",
    )


def test_investigation_adds_interpretation_to_hypothesis() -> None:
    investigation, hypothesis, claim = create_reasoning_chain()
    interpretation = create_interpretation(hypothesis, claim)

    target = investigation.add_interpretation(hypothesis.id, interpretation)

    assert target is hypothesis
    assert hypothesis.interpretations == (interpretation,)


def test_closed_investigation_rejects_interpretation_attachment() -> None:
    investigation, hypothesis, claim = create_reasoning_chain()
    investigation.close()
    investigation.pull_events()
    interpretation = create_interpretation(hypothesis, claim)

    with pytest.raises(ValueError, match="investigation is closed"):
        investigation.add_interpretation(hypothesis.id, interpretation)

    assert hypothesis.interpretations == ()
    assert hypothesis.pull_events() == []


def test_add_interpretation_requires_known_hypothesis() -> None:
    investigation, hypothesis, claim = create_reasoning_chain()
    unknown = Hypothesis(statement="Unknown")
    interpretation = create_interpretation(hypothesis, claim)

    with pytest.raises(LookupError, match="hypothesis not found"):
        investigation.add_interpretation(unknown.id, interpretation)

    assert hypothesis.interpretations == ()
    assert hypothesis.pull_events() == []
