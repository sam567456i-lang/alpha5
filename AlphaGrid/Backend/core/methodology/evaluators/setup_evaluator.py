from typing import Dict, Any
from Backend.core.methodology.evaluators.base_evaluator import BaseEvaluator
from Backend.core.methodology.dto.base_candidate import SetupCandidate
from Backend.core.methodology.dto.base_evaluation import BaseEvaluation, PassedEvaluation, RejectedEvaluation, DeferredEvaluation, ConditionalEvaluation

class SetupEvaluator(BaseEvaluator):
    """
    Evaluates a proposed market setup (e.g. OTE convergence) against policy.
    Migrated from ICTEntryModule.
    """
    def __init__(self, policy_config: Dict[str, Any] = None):
        self.policy_config = policy_config or {}
        
    def evaluate(self, candidate: SetupCandidate, context: Dict[str, Any]) -> BaseEvaluation:
        # Extract inputs from metadata
        metadata = candidate.metadata
        has_dealing_range = metadata.get("has_dealing_range", False)
        has_pd_array = metadata.get("has_pd_array", False)
        requires_session = self.policy_config.get("setup_requires_session", False)
        has_session = metadata.get("has_session_alignment", False)
        is_premium_discount_aligned = metadata.get("is_premium_discount_aligned", False)
        
        # 1. Reject if no valid dealing range or PD array
        if not has_dealing_range or not has_pd_array:
            return RejectedEvaluation(
                evaluator_id="SetupEvaluator",
                rejected_conditions=["Missing Dealing Range or PD Array"]
            )
            
        # 2. Reject if array is misaligned (e.g. buying in Premium)
        if not is_premium_discount_aligned:
            return RejectedEvaluation(
                evaluator_id="SetupEvaluator",
                rejected_conditions=["PD Array is not properly aligned (Discount for longs, Premium for shorts)"]
            )
            
        # 3. Wait for displacement (Deferred) if policy requires it and it hasn't happened
        requires_displacement = self.policy_config.get("setup_requires_displacement", False)
        has_displacement = metadata.get("has_displacement", False)
        if requires_displacement and not has_displacement:
            return DeferredEvaluation(
                evaluator_id="SetupEvaluator",
                waiting_for="Displacement structure break"
            )
            
        # 4. Conditional on session if missing
        if requires_session and not has_session:
            return ConditionalEvaluation(
                evaluator_id="SetupEvaluator",
                conditions=["Requires valid session killzone overlap"]
            )
            
        # 5. Pass
        return PassedEvaluation(
            evaluator_id="SetupEvaluator",
            reasons=["All setup convergences met"],
            metadata={
                "setup_direction": candidate.setup_direction,
                "setup_name": candidate.setup_name,
                "is_active": True
            }
        )
