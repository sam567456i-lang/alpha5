from typing import Dict, Any, List
from Backend.core.methodology.evaluators.base_evaluator import BaseEvaluator
from Backend.core.methodology.dto.base_candidate import AuctionCandidate
from Backend.core.methodology.dto.base_evaluation import BaseEvaluation, PassedEvaluation, RejectedEvaluation

class AuctionEvaluator(BaseEvaluator):
    """
    Evaluates generic volume and time acceptance in a given region.
    """
    def __init__(self, policy_config: Dict[str, Any] = None):
        self.policy_config = policy_config or {}
        self.min_time_accepted = self.policy_config.get("min_time_accepted", 300)
        self.min_rotations_accepted = self.policy_config.get("min_rotations_accepted", 3)
        
    def evaluate(self, candidate: AuctionCandidate, context: Dict[str, Any]) -> BaseEvaluation:
        # Determine if price accepted or rejected the region based on objective metrics
        is_accepted = candidate.time_inside_region > self.min_time_accepted or candidate.rotation_count >= self.min_rotations_accepted
        
        state = "ACCEPTED" if is_accepted else "REJECTED"
        
        return PassedEvaluation(
            evaluator_id="AuctionEvaluator",
            reasons=[f"Region was {state}"],
            metadata={
                "acceptance_state": state,
                "region_type": candidate.region_type,
                "value_area_shift": "MAINTAINED" # simplified
            }
        )
