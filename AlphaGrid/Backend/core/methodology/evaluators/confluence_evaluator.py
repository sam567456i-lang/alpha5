from typing import Dict, Any, List
from Backend.core.methodology.evaluators.base_evaluator import BaseEvaluator
from Backend.core.methodology.dto.base_candidate import ConfluenceCandidate
from Backend.core.methodology.dto.base_evaluation import BaseEvaluation, PassedEvaluation, RejectedEvaluation, DeferredEvaluation

class ConfluenceEvaluator(BaseEvaluator):
    """
    Evaluates ConfluenceCandidates against configured confluence profiles.
    Returns PassedEvaluation with a matched profile identity if components align.
    """
    def __init__(self, policy_config: Dict[str, Any] = None):
        self.policy_config = policy_config or {}
        
        self.configurations = self.policy_config.get("configurations", [
            {"name": "UNICORN", "requires": ["FVG", "Breaker"], "minimum_matches": 2},
            {"name": "DOUBLE_FVG", "requires": ["FVG", "FVG"], "minimum_matches": 2}
        ])
        
    def evaluate(self, candidate: ConfluenceCandidate, context: Dict[str, Any]) -> BaseEvaluation:
        candidate_arrays = list(candidate.component_types)
        
        matched_configs = []
        
        for config in self.configurations:
            available_arrays = list(candidate_arrays)
            matches = True
            matched_count = 0
            
            for req in config.get("requires", []):
                if req in available_arrays:
                    available_arrays.remove(req)
                    matched_count += 1
                else:
                    matches = False
                    break
                    
            if matches and matched_count >= config.get("minimum_matches", len(config.get("requires", []))):
                matched_configs.append(config["name"])
                
        if not matched_configs:
            return RejectedEvaluation(
                evaluator_id="ConfluenceEvaluator",
                rejected_conditions=["Candidate components do not match any known confluence profile"]
            )
            
        if len(matched_configs) > 1:
            # Ambiguous match (e.g. FVG + FVG + Breaker could be Unicorn AND Double FVG)
            # Passed, but metadata reflects ambiguity
            pass
            
        return PassedEvaluation(
            evaluator_id="ConfluenceEvaluator",
            reasons=["Matched confluence configuration(s)"],
            metadata={
                "matched_profiles": matched_configs,
                "component_candidate_ids": candidate.component_candidate_ids
            }
        )
