from uuid import UUID

import pytest

from titan.core.evidence import Evidence


def test_create_evidence() -> None:
    evidence = Evidence(
        description="Firewall logs show repeated failed logins.",
        source="Authentication server logs",
    )

    assert evidence.description == ("Firewall logs show repeated failed logins.")
    assert evidence.source == "Authentication server logs"
    assert isinstance(evidence.id.value, UUID)


def test_evidence_requires_description() -> None:
    with pytest.raises(
        ValueError,
        match="description must not be empty",
    ):
        Evidence(
            description="   ",
            source="Authentication server logs",
        )


def test_evidence_requires_source() -> None:
    with pytest.raises(
        ValueError,
        match="source must not be empty",
    ):
        Evidence(
            description="Firewall logs show repeated failed logins.",
            source="   ",
        )
