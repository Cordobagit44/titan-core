from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Hypothesis:
    statement: str

    def __post_init__(self) -> None:
        if not self.statement.strip():
            raise ValueError("statement must not be empty")
