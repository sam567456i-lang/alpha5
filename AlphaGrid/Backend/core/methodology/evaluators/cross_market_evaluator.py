from typing import Dict, Any, List
from Backend.core.methodology.evaluators.base_evaluator import BaseEvaluator
from Backend.core.methodology.dto.base_candidate import CrossMarketCandidate
from Backend.core.methodology.dto.base_evaluation import BaseEvaluation, PassedEvaluation, RejectedEvaluation

class CrossMarketEvaluator(BaseEvaluator):
    """
    Evaluates generic structural divergences between two correlated assets.
    """
    def __init__(self, policy_config: Dict[str, Any] = None):
        self.policy_config = policy_config or {}
        
    def evaluate(self, candidate: CrossMarketCandidate, context: Dict[str, Any]) -> BaseEvaluation:
        prim = candidate.primary_structure_state
        sec = candidate.secondary_structure_state
        
        div_type = None
        bias = None
        
        if prim == "HIGHER_HIGH" and sec == "LOWER_HIGH":
            div_type = "HIGHER_HIGH_VS_LOWER_HIGH"
            bias = "BULLISH" # Weakness in secondary implies primary is strong
        elif prim == "LOWER_LOW" and sec == "HIGHER_LOW":
            div_type = "LOWER_LOW_VS_HIGHER_LOW"
            bias = "BEARISH"
        
        if not div_type:
            return RejectedEvaluation(
                evaluator_id="CrossMarketEvaluator",
                rejected_conditions=["No recognized structural divergence found between primary and secondary assets"]
            )
            
        return PassedEvaluation(
            evaluator_id="CrossMarketEvaluator",
            reasons=["Divergence identified"],
            metadata={
                "divergence_type": div_type,
                "primary_symbol": candidate.primary_symbol,
                "secondary_symbol": candidate.secondary_symbol,
                "bias_indication": bias
            }
        )
