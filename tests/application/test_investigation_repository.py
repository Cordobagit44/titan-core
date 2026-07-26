from inspect import isabstract

from titan.application.investigation_repository import (
    InvestigationRepository,
)


def test_repository_is_abstract() -> None:
    assert isabstract(InvestigationRepository)
