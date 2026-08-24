import pytest

from titan.core.investigation import Investigation, ThesisAdded
from titan.core.thesis import Thesis


@pytest.mark.parametrize("activate", [False, True])
def test_open_investigation_adds_thesis(activate: bool) -> None:
    investigation = Investigation.create("Mars anomaly", "Evaluate evidence")
    if activate:
        investigation.activate()
    thesis = Thesis(statement="The anomaly is most likely geological.")

    investigation.add_thesis(thesis)

    assert investigation.theses == (thesis,)


def test_adding_thesis_emits_domain_event() -> None:
    investigation = Investigation.create("Mars anomaly", "Evaluate evidence")
    investigation.pull_events()
    thesis = Thesis(statement="The anomaly is most likely geological.")

    investigation.add_thesis(thesis)

    assert investigation.pull_events() == [
        ThesisAdded(
            investigation_id=investigation.id,
            thesis_id=thesis.id,
        )
    ]


def test_investigation_rejects_duplicate_thesis_identifier() -> None:
    investigation = Investigation.create("Mars anomaly", "Evaluate evidence")
    thesis = Thesis(statement="The anomaly is most likely geological.")
    investigation.add_thesis(thesis)
    investigation.pull_events()

    with pytest.raises(ValueError, match="thesis already exists"):
        investigation.add_thesis(thesis)

    assert investigation.theses == (thesis,)
    assert investigation.pull_events() == []


def test_closed_investigation_rejects_thesis() -> None:
    investigation = Investigation.create("Mars anomaly", "Evaluate evidence")
    investigation.close()
    investigation.pull_events()
    thesis = Thesis(statement="The anomaly is most likely geological.")

    with pytest.raises(ValueError, match="investigation is closed"):
        investigation.add_thesis(thesis)

    assert investigation.theses == ()
    assert investigation.pull_events() == []


def test_equal_thesis_statements_can_have_distinct_identities() -> None:
    investigation = Investigation.create("Mars anomaly", "Evaluate evidence")
    first = Thesis(statement="The anomaly is most likely geological.")
    second = Thesis(statement=first.statement)

    investigation.add_thesis(first)
    investigation.add_thesis(second)

    assert investigation.theses == (first, second)
