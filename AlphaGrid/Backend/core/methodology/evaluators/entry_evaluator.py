from typing import Dict, Any
from Backend.core.methodology.evaluators.base_evaluator import BaseEvaluator
from Backend.core.methodology.dto.base_candidate import EntryCandidate
from Backend.core.methodology.dto.base_evaluation import BaseEvaluation, PassedEvaluation, RejectedEvaluation

class EntryEvaluator(BaseEvaluator):
    """
    Evaluates an EntryCandidate (e.g. proposed limit order) against execution policies.
    Migrated from ICTEntryModule.
    """
    def __init__(self, policy_config: Dict[str, Any] = None):
        self.policy_config = policy_config or {}
        
    def evaluate(self, candidate: EntryCandidate, context: Dict[str, Any]) -> BaseEvaluation:
        # Evaluate execution boundaries
        min_fib = self.policy_config.get("ote_min_fib_level", 0.62)
        max_fib = self.policy_config.get("ote_max_fib_level", 0.79)
        
        fib = candidate.fib_level
        
        if fib < min_fib or fib > max_fib:
            return RejectedEvaluation(
                evaluator_id="EntryEvaluator",
                rejected_conditions=[f"Fib level {fib} outside OTE boundaries ({min_fib}-{max_fib})"]
            )
            
        return PassedEvaluation(
            evaluator_id="EntryEvaluator",
            reasons=["Entry parameters within OTE boundaries"],
            metadata={
                "entry_type": candidate.entry_type,
                "entry_price": candidate.entry_price,
                "stop_loss_price": candidate.stop_loss_price,
                "target_price": candidate.target_price
            }
        )
