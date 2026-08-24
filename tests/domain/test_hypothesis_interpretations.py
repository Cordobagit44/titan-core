import pytest

from titan.core.claim import Claim, ClaimId
from titan.core.events import InterpretationAdded
from titan.core.evidence import Evidence, EvidenceRelationship
from titan.core.hypothesis import Hypothesis, HypothesisStatus
from titan.core.interpretation import Interpretation


def create_hypothesis_with_claim() -> tuple[Hypothesis, Claim]:
    hypothesis = Hypothesis(statement="Methane indicates microbial activity")
    evidence = Evidence(
        description="Methane varies seasonally",
        source="Mars orbiter",
        relationship=EvidenceRelationship.SUPPORTS,
    )
    hypothesis.add_evidence(evidence)
    hypothesis.pull_events()
    claim = Claim(statement="Methane varies seasonally", evidence_id=evidence.id)
    hypothesis.add_claim(claim)
    hypothesis.pull_events()
    return hypothesis, claim


def create_interpretation(hypothesis: Hypothesis, claim_id: ClaimId) -> Interpretation:
    return Interpretation(
        hypothesis_id=hypothesis.id,
        claim_id=claim_id,
        rationale="Seasonal variation is consistent with a biological cycle.",
    )


def test_hypothesis_adds_interpretation() -> None:
    hypothesis, claim = create_hypothesis_with_claim()
    interpretation = create_interpretation(hypothesis, claim.id)

    hypothesis.add_interpretation(interpretation)

    assert hypothesis.interpretations == (interpretation,)


def test_adding_interpretation_emits_domain_event() -> None:
    hypothesis, claim = create_hypothesis_with_claim()
    interpretation = create_interpretation(hypothesis, claim.id)

    hypothesis.add_interpretation(interpretation)

    assert hypothesis.pull_events() == [
        InterpretationAdded(
            hypothesis_id=hypothesis.id,
            interpretation_id=interpretation.id,
            claim_id=claim.id,
        )
    ]


def test_hypothesis_rejects_interpretation_for_another_hypothesis() -> None:
    hypothesis, claim = create_hypothesis_with_claim()
    other = Hypothesis(statement="Methane has an abiotic cause")
    interpretation = Interpretation(
        hypothesis_id=other.id,
        claim_id=claim.id,
        rationale="Seasonal variation is consistent with a biological cycle.",
    )

    with pytest.raises(
        LookupError,
        match="interpretation hypothesis does not match",
    ):
        hypothesis.add_interpretation(interpretation)

    assert hypothesis.interpretations == ()
    assert hypothesis.pull_events() == []


def test_hypothesis_rejects_interpretation_for_unknown_claim() -> None:
    hypothesis, _ = create_hypothesis_with_claim()
    interpretation = create_interpretation(hypothesis, ClaimId.new())

    with pytest.raises(LookupError, match="interpretation claim not found"):
        hypothesis.add_interpretation(interpretation)

    assert hypothesis.interpretations == ()
    assert hypothesis.pull_events() == []


def test_hypothesis_rejects_duplicate_interpretation_identifier() -> None:
    hypothesis, claim = create_hypothesis_with_claim()
    interpretation = create_interpretation(hypothesis, claim.id)
    hypothesis.add_interpretation(interpretation)
    hypothesis.pull_events()

    with pytest.raises(ValueError, match="interpretation already exists"):
        hypothesis.add_interpretation(interpretation)

    assert hypothesis.interpretations == (interpretation,)
    assert hypothesis.pull_events() == []


@pytest.mark.parametrize(
    "status",
    [HypothesisStatus.CONFIRMED, HypothesisStatus.REJECTED],
)
def test_decided_hypothesis_rejects_new_interpretation(
    status: HypothesisStatus,
) -> None:
    hypothesis, claim = create_hypothesis_with_claim()
    if status is HypothesisStatus.CONFIRMED:
        hypothesis.confirm()
    else:
        hypothesis.reject()
    hypothesis.pull_events()
    interpretation = create_interpretation(hypothesis, claim.id)

    with pytest.raises(
        ValueError,
        match="decided hypothesis cannot accept interpretations",
    ):
        hypothesis.add_interpretation(interpretation)

    assert hypothesis.interpretations == ()
    assert hypothesis.pull_events() == []


def test_equal_rationale_can_have_distinct_interpretation_identities() -> None:
    hypothesis, claim = create_hypothesis_with_claim()
    first = create_interpretation(hypothesis, claim.id)
    second = create_interpretation(hypothesis, claim.id)

    hypothesis.add_interpretation(first)
    hypothesis.add_interpretation(second)

    assert hypothesis.interpretations == (first, second)
