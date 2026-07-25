from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass(frozen=True)
class HypothesisId:
    value: UUID

    @classmethod
    def new(cls) -> "HypothesisId":
        return cls(value=uuid4())


@dataclass(frozen=True)
class Hypothesis:
    statement: str
    id: HypothesisId = field(default_factory=HypothesisId.new)

    def __post_init__(self) -> None:
        if not self.statement.strip():
            raise ValueError("statement must not be empty")
