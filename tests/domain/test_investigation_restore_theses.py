import pytest

from titan.core.investigation import (
    Investigation,
    InvestigationId,
    InvestigationStatus,
)
from titan.core.thesis import Thesis


def test_restore_rejects_duplicate_thesis_identity() -> None:
    first = Thesis(statement="Initial conclusion")
    duplicate = Thesis(
        id=first.id,
        statement="Different statement with the same identity",
    )

    with pytest.raises(ValueError, match="thesis already exists"):
        Investigation.restore(
            investigation_id=InvestigationId.new(),
            title="Mars anomaly",
            purpose="Evaluate evidence",
            status=InvestigationStatus.DRAFT,
            hypotheses=(),
            theses=(first, duplicate),
        )


def test_restore_accepts_distinct_thesis_identities() -> None:
    theses = (
        Thesis(statement="Initial conclusion"),
        Thesis(statement="Alternative conclusion"),
    )

    investigation = Investigation.restore(
        investigation_id=InvestigationId.new(),
        title="Mars anomaly",
        purpose="Evaluate evidence",
        status=InvestigationStatus.DRAFT,
        hypotheses=(),
        theses=theses,
    )

    assert investigation.theses == theses
    assert investigation.pull_events() == []
