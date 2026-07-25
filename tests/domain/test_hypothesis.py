from uuid import UUID

import pytest

from titan.core.hypothesis import Hypothesis


def test_create_hypothesis() -> None:
    hypothesis = Hypothesis(
        statement="NVIDIA will maintain 20% annual revenue growth.",
    )

    assert hypothesis.statement == ("NVIDIA will maintain 20% annual revenue growth.")


@pytest.mark.parametrize("invalid_statement", ["", "   "])
def test_hypothesis_rejects_empty_statement(
    invalid_statement: str,
) -> None:
    with pytest.raises(ValueError, match="statement must not be empty"):
        Hypothesis(statement=invalid_statement)


def test_hypothesis_receives_an_identifier() -> None:
    hypothesis = Hypothesis(
        statement="Credentials were compromised",
    )

    assert isinstance(hypothesis.id.value, UUID)


def test_hypotheses_receive_different_identifiers() -> None:
    first = Hypothesis(
        statement="Credentials were compromised",
    )
    second = Hypothesis(
        statement="Malware was delivered by email",
    )

    assert first.id != second.id
