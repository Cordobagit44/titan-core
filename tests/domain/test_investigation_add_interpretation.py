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


def test_investigation_rejects_interpretation_reused_across_hypotheses() -> None:
    investigation, first, first_claim = create_reasoning_chain()
    first_interpretation = create_interpretation(first, first_claim)
    investigation.add_interpretation(first.id, first_interpretation)
    first.pull_events()

    investigation.add_hypothesis("Methane has an abiotic cause")
    second = investigation.hypotheses[1]
    second_evidence = Evidence(
        description="Methane appears near geological faults",
        source="Mars rover",
        relationship=EvidenceRelationship.SUPPORTS,
    )
    investigation.add_evidence(second.id, second_evidence)
    second_claim = Claim(
        statement="Geology can produce methane",
        evidence_id=second_evidence.id,
    )
    investigation.add_claim(second.id, second_claim)
    second.pull_events()
    reused = Interpretation(
        id=first_interpretation.id,
        hypothesis_id=second.id,
        claim_id=second_claim.id,
        rationale="Geological activity explains the observed methane.",
    )

    with pytest.raises(
        ValueError,
        match="interpretation already belongs to another hypothesis",
    ):
        investigation.add_interpretation(second.id, reused)

    assert second.interpretations == ()
    assert second.pull_events() == []
