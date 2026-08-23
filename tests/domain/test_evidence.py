from uuid import UUID

import pytest

from titan.core.evidence import (
    Evidence,
    EvidenceRelationship,
)


def test_create_supporting_evidence() -> None:
    evidence = Evidence(
        description="Firewall logs show repeated failed logins.",
        source="Authentication server logs",
        relationship=EvidenceRelationship.SUPPORTS,
    )

    assert evidence.description == ("Firewall logs show repeated failed logins.")
    assert evidence.source == "Authentication server logs"
    assert evidence.relationship is EvidenceRelationship.SUPPORTS
    assert isinstance(evidence.id.value, UUID)


def test_create_weakening_evidence() -> None:
    evidence = Evidence(
        description="No suspicious login pattern was observed.",
        source="Authentication server logs",
        relationship=EvidenceRelationship.WEAKENS,
    )

    assert evidence.relationship is EvidenceRelationship.WEAKENS


def test_evidence_requires_description() -> None:
    with pytest.raises(
        ValueError,
        match="description must not be empty",
    ):
        Evidence(
            description="   ",
            source="Authentication server logs",
            relationship=EvidenceRelationship.SUPPORTS,
        )


def test_evidence_requires_source() -> None:
    with pytest.raises(
        ValueError,
        match="source must not be empty",
    ):
        Evidence(
            description="Firewall logs show repeated failed logins.",
            source="   ",
            relationship=EvidenceRelationship.SUPPORTS,
        )


def test_evidence_can_restore_unspecified_relationship() -> None:
    evidence = Evidence(
        description="Legacy evidence",
        source="legacy source unavailable",
        relationship=EvidenceRelationship.UNSPECIFIED,
    )

    assert evidence.relationship is EvidenceRelationship.UNSPECIFIED
