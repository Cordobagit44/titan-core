from dataclasses import dataclass, field
from enum import Enum
from uuid import UUID, uuid4


class EvidenceRelationship(Enum):
    SUPPORTS = "supports"
    WEAKENS = "weakens"
    UNSPECIFIED = "unspecified"


@dataclass(frozen=True)
class EvidenceId:
    value: UUID

    @classmethod
    def new(cls) -> "EvidenceId":
        return cls(
            value=uuid4(),
        )


@dataclass(frozen=True)
class Evidence:
    description: str
    source: str
    relationship: EvidenceRelationship
    id: EvidenceId = field(
        default_factory=EvidenceId.new,
    )

    def __post_init__(
        self,
    ) -> None:
        if not self.description.strip():
            raise ValueError(
                "description must not be empty",
            )

        if not self.source.strip():
            raise ValueError(
                "source must not be empty",
            )
