from pathlib import Path

from titan.bootstrap import bootstrap
from titan.core.investigation import InvestigationStatus


def test_bootstrap_wires_sqlite_application(
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
        purpose="Find evidence",
    )

    application.activate_investigation(
        investigation.id,
    )

    restored = application.get_investigation(
        investigation.id,
    )

    assert restored.id == investigation.id
    assert restored.status is InvestigationStatus.ACTIVE

    listed = application.list_investigations()

    assert len(listed) == 1
    assert listed[0].id == restored.id
    assert listed[0].status is InvestigationStatus.ACTIVE


def test_bootstrap_exposes_application_use_cases(
    tmp_path: Path,
) -> None:
    application = bootstrap(
        str(
            tmp_path / "titan.db",
        )
    )

    assert callable(application.create_investigation)
    assert callable(application.activate_investigation)
    assert callable(application.add_hypothesis)
    assert callable(application.add_evidence)
    assert callable(application.confirm_hypothesis)
    assert callable(application.reject_hypothesis)
    assert callable(application.remove_hypothesis)
    assert callable(application.close_investigation)
    assert callable(application.reopen_investigation)
    assert callable(application.get_investigation)
    assert callable(application.list_investigations)
