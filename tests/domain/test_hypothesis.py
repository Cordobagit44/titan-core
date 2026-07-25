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
