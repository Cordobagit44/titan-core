from inspect import isabstract

from titan.application.unit_of_work import UnitOfWork


def test_unit_of_work_is_abstract() -> None:
    assert isabstract(UnitOfWork)


def test_unit_of_work_defines_required_contract() -> None:
    assert UnitOfWork.__abstractmethods__ == {
        "commit",
        "domain_events",
        "investigations",
        "rollback",
    }
