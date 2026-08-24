from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass(frozen=True)
class ThesisId:
    value: UUID

    @classmethod
    def new(cls) -> "ThesisId":
        return cls(value=uuid4())


@dataclass(frozen=True)
class Thesis:
    statement: str
    id: ThesisId = field(default_factory=ThesisId.new)

    def __post_init__(self) -> None:
        if not self.statement.strip():
            raise ValueError("statement must not be empty")
