from pathlib import Path

from titan.bootstrap import bootstrap
from titan.core.evidence import EvidenceRelationship
from titan.core.hypothesis import HypothesisStatus
from titan.core.investigation import InvestigationStatus


def test_complete_investigation_workflow_is_persisted(
    tmp_path: Path,
) -> None:
    database = str(
        tmp_path / "titan.db",
    )

    application = bootstrap(
        database,
    )

    investigation = application.create_investigation(
        title="Mars anomaly",
        purpose="Evaluate evidence for microbial activity",
    )

    application.activate_investigation(
        investigation.id,
    )

    hypothesis = application.add_hypothesis(
        investigation_id=investigation.id,
        statement="Seasonal methane variation indicates microbial activity",
    )

    evidence = application.add_evidence(
        investigation_id=investigation.id,
        hypothesis_id=hypothesis.id,
        description="Methane concentration varies seasonally",
        source="NASA Curiosity methane measurements",
        relationship=EvidenceRelationship.SUPPORTS,
    )

    claim = application.add_claim(
        investigation_id=investigation.id,
        hypothesis_id=hypothesis.id,
        evidence_id=evidence.id,
        statement="Methane concentration varies seasonally",
    )

    interpretation = application.add_interpretation(
        investigation_id=investigation.id,
        hypothesis_id=hypothesis.id,
        claim_id=claim.id,
        rationale="Seasonality makes a biological mechanism plausible",
    )

    application.confirm_hypothesis(
        investigation_id=investigation.id,
        hypothesis_id=hypothesis.id,
    )

    application.close_investigation(
        investigation.id,
    )

    application.close()

    restarted_application = bootstrap(
        database,
    )

    restored = restarted_application.get_investigation(
        investigation.id,
    )

    assert restored.id == investigation.id
    assert restored.title == "Mars anomaly"
    assert restored.purpose == "Evaluate evidence for microbial activity"
    assert restored.status is InvestigationStatus.CLOSED
    assert restored.closed_at is not None

    assert len(restored.hypotheses) == 1

    restored_hypothesis = restored.hypotheses[0]

    assert restored_hypothesis.id == hypothesis.id
    assert (
        restored_hypothesis.statement == "Seasonal methane variation indicates microbial activity"
    )
    assert restored_hypothesis.status is HypothesisStatus.CONFIRMED

    assert len(restored_hypothesis.evidences) == 1

    restored_evidence = restored_hypothesis.evidences[0]

    assert restored_evidence.id == evidence.id
    assert restored_evidence.description == "Methane concentration varies seasonally"
    assert restored_evidence.source == "NASA Curiosity methane measurements"
    assert restored_evidence.relationship is EvidenceRelationship.SUPPORTS

    assert len(restored_hypothesis.claims) == 1

    restored_claim = restored_hypothesis.claims[0]

    assert restored_claim.id == claim.id
    assert restored_claim.statement == "Methane concentration varies seasonally"
    assert restored_claim.evidence_id == evidence.id

    assert len(restored_hypothesis.interpretations) == 1

    restored_interpretation = restored_hypothesis.interpretations[0]

    assert restored_interpretation.id == interpretation.id
    assert restored_interpretation.rationale == "Seasonality makes a biological mechanism plausible"
    assert restored_interpretation.claim_id == claim.id
    assert restored_interpretation.hypothesis_id == hypothesis.id

    listed = restarted_application.list_investigations()

    assert len(listed) == 1
    assert listed[0].id == investigation.id

    restarted_application.close()
