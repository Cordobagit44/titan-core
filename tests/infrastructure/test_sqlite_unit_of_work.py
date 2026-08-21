from pathlib import Path

from titan.core.investigation import Investigation
from titan.infrastructure.sqlite.sqlite_unit_of_work import (
    SqliteUnitOfWork,
)


def test_commit_persists_investigation_and_domain_event(
    tmp_path: Path,
) -> None:
    database = str(
        tmp_path / "unit_of_work.db",
    )

    unit_of_work = SqliteUnitOfWork(
        database,
    )

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    created_event = investigation.pull_events()[0]

    unit_of_work.investigations.save(
        investigation,
    )
    unit_of_work.domain_events.save(
        created_event,
    )

    unit_of_work.commit()

    restored = SqliteUnitOfWork(
        database,
    )

    restored_investigation = restored.investigations.get(
        investigation.id,
    )

    assert restored_investigation is not None
    assert restored_investigation.id == investigation.id
    assert restored_investigation.title == investigation.title
    assert restored_investigation.purpose == investigation.purpose
    assert restored_investigation.status == investigation.status

    assert restored.domain_events.list_all() == [
        created_event,
    ]


def test_rollback_discards_investigation_and_domain_event(
    tmp_path: Path,
) -> None:
    database = str(
        tmp_path / "unit_of_work.db",
    )

    unit_of_work = SqliteUnitOfWork(
        database,
    )

    investigation = Investigation.create(
        title="Mars anomaly",
        purpose="Find evidence",
    )
    created_event = investigation.pull_events()[0]

    unit_of_work.investigations.save(
        investigation,
    )
    unit_of_work.domain_events.save(
        created_event,
    )

    unit_of_work.rollback()

    restored = SqliteUnitOfWork(
        database,
    )

    assert (
        restored.investigations.get(
            investigation.id,
        )
        is None
    )

    assert restored.domain_events.list_all() == []
