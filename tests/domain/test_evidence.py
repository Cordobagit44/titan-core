from uuid import UUID

from titan.core.evidence import Evidence


def test_create_evidence() -> None:
    evidence = Evidence(
        description="Firewall logs show repeated failed logins.",
    )

    assert evidence.description == ("Firewall logs show repeated failed logins.")
    assert isinstance(evidence.id.value, UUID)
