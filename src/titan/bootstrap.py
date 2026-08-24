from __future__ import annotations

from dataclasses import dataclass

from titan.application.activate_investigation import ActivateInvestigation
from titan.application.add_claim import AddClaim
from titan.application.add_evidence import AddEvidence
from titan.application.add_hypothesis import AddHypothesis
from titan.application.close_investigation import CloseInvestigation
from titan.application.confirm_hypothesis import ConfirmHypothesis
from titan.application.create_investigation import CreateInvestigation
from titan.application.get_investigation import GetInvestigation
from titan.application.list_investigations import ListInvestigations
from titan.application.reject_hypothesis import RejectHypothesis
from titan.application.remove_hypothesis import RemoveHypothesis
from titan.application.reopen_investigation import ReopenInvestigation
from titan.infrastructure.sqlite.sqlite_unit_of_work import (
    SqliteUnitOfWork,
)


@dataclass(frozen=True)
class TitanApplication:
    create_investigation: CreateInvestigation
    activate_investigation: ActivateInvestigation
    add_hypothesis: AddHypothesis
    add_evidence: AddEvidence
    add_claim: AddClaim
    confirm_hypothesis: ConfirmHypothesis
    reject_hypothesis: RejectHypothesis
    remove_hypothesis: RemoveHypothesis
    close_investigation: CloseInvestigation
    reopen_investigation: ReopenInvestigation
    get_investigation: GetInvestigation
    list_investigations: ListInvestigations
    _unit_of_work: SqliteUnitOfWork

    def close(
        self,
    ) -> None:
        self._unit_of_work.close()


def bootstrap(
    database: str,
) -> TitanApplication:
    unit_of_work = SqliteUnitOfWork(
        database,
    )

    investigations = unit_of_work.investigations

    return TitanApplication(
        create_investigation=CreateInvestigation(
            unit_of_work,
        ),
        activate_investigation=ActivateInvestigation(
            unit_of_work,
        ),
        add_hypothesis=AddHypothesis(
            unit_of_work,
        ),
        add_evidence=AddEvidence(
            unit_of_work,
        ),
        add_claim=AddClaim(
            unit_of_work,
        ),
        confirm_hypothesis=ConfirmHypothesis(
            unit_of_work,
        ),
        reject_hypothesis=RejectHypothesis(
            unit_of_work,
        ),
        remove_hypothesis=RemoveHypothesis(
            unit_of_work,
        ),
        close_investigation=CloseInvestigation(
            unit_of_work,
        ),
        reopen_investigation=ReopenInvestigation(
            unit_of_work,
        ),
        get_investigation=GetInvestigation(
            investigations,
        ),
        list_investigations=ListInvestigations(
            investigations,
        ),
        _unit_of_work=unit_of_work,
    )
