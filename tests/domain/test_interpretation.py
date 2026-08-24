from uuid import UUID

import pytest

from titan.core.claim import ClaimId
from titan.core.hypothesis import HypothesisId
from titan.core.interpretation import Interpretation, InterpretationId


def test_create_interpretation() -> None:
    claim_id = ClaimId.new()
    hypothesis_id = HypothesisId.new()

    interpretation = Interpretation(
        claim_id=claim_id,
        hypothesis_id=hypothesis_id,
        rationale="Seasonal variation is consistent with a biological cycle.",
    )

    assert interpretation.claim_id == claim_id
    assert interpretation.hypothesis_id == hypothesis_id
    assert interpretation.rationale == ("Seasonal variation is consistent with a biological cycle.")
    assert isinstance(interpretation.id.value, UUID)


def test_interpretation_requires_rationale() -> None:
    with pytest.raises(ValueError, match="rationale must not be empty"):
        Interpretation(
            claim_id=ClaimId.new(),
            hypothesis_id=HypothesisId.new(),
            rationale="   ",
        )


def test_interpretation_can_restore_explicit_identity() -> None:
    interpretation_id = InterpretationId.new()

    interpretation = Interpretation(
        id=interpretation_id,
        claim_id=ClaimId.new(),
        hypothesis_id=HypothesisId.new(),
        rationale="The claim supports the hypothesis.",
    )

    assert interpretation.id == interpretation_id


def test_separately_created_interpretations_have_distinct_identities() -> None:
    claim_id = ClaimId.new()
    hypothesis_id = HypothesisId.new()

    first = Interpretation(
        claim_id=claim_id,
        hypothesis_id=hypothesis_id,
        rationale="The claim supports the hypothesis.",
    )
    second = Interpretation(
        claim_id=claim_id,
        hypothesis_id=hypothesis_id,
        rationale=first.rationale,
    )

    assert first.id != second.id
