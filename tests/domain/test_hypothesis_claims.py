import pytest

from titan.core.claim import Claim
from titan.core.events import ClaimAdded
from titan.core.evidence import Evidence, EvidenceRelationship
from titan.core.hypothesis import Hypothesis, HypothesisStatus


def create_evidence() -> Evidence:
    return Evidence(
        description="Seasonal methane variation was observed.",
        source="Mars orbiter",
        relationship=EvidenceRelationship.SUPPORTS,
    )


def create_grounded_hypothesis() -> tuple[Hypothesis, Evidence]:
    hypothesis = Hypothesis(statement="Methane indicates microbial activity")
    evidence = create_evidence()
    hypothesis.add_evidence(evidence)
    hypothesis.pull_events()
    return hypothesis, evidence


def test_hypothesis_adds_evidence_grounded_claim() -> None:
    hypothesis, evidence = create_grounded_hypothesis()
    claim = Claim(statement="Methane varies seasonally", evidence_id=evidence.id)

    hypothesis.add_claim(claim)

    assert hypothesis.claims == (claim,)


def test_adding_claim_emits_domain_event() -> None:
    hypothesis, evidence = create_grounded_hypothesis()
    claim = Claim(statement="Methane varies seasonally", evidence_id=evidence.id)

    hypothesis.add_claim(claim)

    assert hypothesis.pull_events() == [
        ClaimAdded(
            hypothesis_id=hypothesis.id,
            claim_id=claim.id,
            evidence_id=evidence.id,
        )
    ]


def test_hypothesis_rejects_claim_with_unknown_evidence() -> None:
    hypothesis = Hypothesis(statement="Methane indicates microbial activity")
    claim = Claim(
        statement="Methane varies seasonally",
        evidence_id=create_evidence().id,
    )

    with pytest.raises(LookupError, match="claim evidence not found"):
        hypothesis.add_claim(claim)

    assert hypothesis.claims == ()
    assert hypothesis.pull_events() == []


def test_hypothesis_rejects_duplicate_claim_identifier() -> None:
    hypothesis, evidence = create_grounded_hypothesis()
    claim = Claim(statement="Methane varies seasonally", evidence_id=evidence.id)
    hypothesis.add_claim(claim)
    hypothesis.pull_events()

    with pytest.raises(ValueError, match="claim already exists"):
        hypothesis.add_claim(claim)

    assert hypothesis.claims == (claim,)
    assert hypothesis.pull_events() == []


@pytest.mark.parametrize(
    "status",
    [HypothesisStatus.CONFIRMED, HypothesisStatus.REJECTED],
)
def test_decided_hypothesis_rejects_new_claim(status: HypothesisStatus) -> None:
    hypothesis, evidence = create_grounded_hypothesis()
    if status is HypothesisStatus.CONFIRMED:
        hypothesis.confirm()
    else:
        hypothesis.reject()
    hypothesis.pull_events()
    claim = Claim(statement="Methane varies seasonally", evidence_id=evidence.id)

    with pytest.raises(
        ValueError,
        match="decided hypothesis cannot accept claims",
    ):
        hypothesis.add_claim(claim)

    assert hypothesis.claims == ()
    assert hypothesis.pull_events() == []


def test_matching_claim_statements_can_have_distinct_identities() -> None:
    hypothesis, evidence = create_grounded_hypothesis()
    first = Claim(statement="Methane varies seasonally", evidence_id=evidence.id)
    second = Claim(statement=first.statement, evidence_id=evidence.id)

    hypothesis.add_claim(first)
    hypothesis.add_claim(second)

    assert hypothesis.claims == (first, second)
