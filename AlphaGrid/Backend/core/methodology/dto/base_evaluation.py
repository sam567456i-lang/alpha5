from dataclasses import dataclass, field
from typing import List, Optional

@dataclass(frozen=True)
class BaseEvaluation:
    """
    Result of evaluating a policy against a candidate.
    """
    evaluator_id: str
    reasons: List[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

@dataclass(frozen=True)
class PassedEvaluation(BaseEvaluation):
    pass

@dataclass(frozen=True)
class RejectedEvaluation(BaseEvaluation):
    rejected_conditions: List[str] = field(default_factory=list)

@dataclass(frozen=True)
class DeferredEvaluation(BaseEvaluation):
    waiting_for: str = ""

@dataclass(frozen=True)
class ConditionalEvaluation(BaseEvaluation):
    conditions: List[str] = field(default_factory=list)
