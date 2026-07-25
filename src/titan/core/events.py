from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from titan.core.hypothesis import HypothesisId


@dataclass(frozen=True)
class HypothesisConfirmed:
    hypothesis_id: "HypothesisId"


@dataclass(frozen=True)
class HypothesisRejected:
    hypothesis_id: "HypothesisId"
