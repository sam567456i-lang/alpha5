from typing import Dict, Any
from Backend.core.methodology.dto.base_candidate import BaseCandidate
from Backend.core.methodology.dto.base_evaluation import BaseEvaluation

class BaseEvaluator:
    """
    Abstract base class for executing a policy against a candidate.
    """
    def evaluate(self, candidate: BaseCandidate, context: Dict[str, Any]) -> BaseEvaluation:
        raise NotImplementedError("Subclasses must implement evaluate()")
