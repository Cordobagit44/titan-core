from uuid import UUID

import pytest

from titan.core.thesis import Thesis, ThesisId


def test_create_provisional_thesis() -> None:
    thesis = Thesis(
        statement="The observed anomaly is more likely geological than artificial.",
    )

    assert thesis.statement == ("The observed anomaly is more likely geological than artificial.")
    assert isinstance(thesis.id.value, UUID)


def test_thesis_requires_statement() -> None:
    with pytest.raises(ValueError, match="statement must not be empty"):
        Thesis(statement="   ")


def test_thesis_can_restore_explicit_identity() -> None:
    thesis_id = ThesisId.new()

    thesis = Thesis(
        id=thesis_id,
        statement="The geological explanation remains provisional.",
    )

    assert thesis.id == thesis_id


def test_separately_created_theses_have_distinct_identities() -> None:
    first = Thesis(statement="The geological explanation is stronger.")
    second = Thesis(statement=first.statement)

    assert first.id != second.id
