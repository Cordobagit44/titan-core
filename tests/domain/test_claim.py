from uuid import UUID

import pytest

from titan.core.claim import Claim, ClaimId
from titan.core.evidence import EvidenceId


def test_create_evidence_grounded_claim() -> None:
    evidence_id = EvidenceId.new()

    claim = Claim(
        statement="Seasonal methane variation was observed.",
        evidence_id=evidence_id,
    )

    assert claim.statement == "Seasonal methane variation was observed."
    assert claim.evidence_id == evidence_id
    assert isinstance(claim.id.value, UUID)


def test_claim_requires_statement() -> None:
    with pytest.raises(ValueError, match="statement must not be empty"):
        Claim(
            statement="   ",
            evidence_id=EvidenceId.new(),
        )


def test_claim_can_restore_explicit_identity() -> None:
    claim_id = ClaimId.new()

    claim = Claim(
        id=claim_id,
        statement="Seasonal methane variation was observed.",
        evidence_id=EvidenceId.new(),
    )

    assert claim.id == claim_id


def test_separately_created_claims_have_distinct_identities() -> None:
    evidence_id = EvidenceId.new()

    first = Claim(statement="Methane was observed.", evidence_id=evidence_id)
    second = Claim(statement="Methane was observed.", evidence_id=evidence_id)

    assert first.id != second.id
