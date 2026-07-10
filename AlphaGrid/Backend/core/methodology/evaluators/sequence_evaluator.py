from typing import Dict, Any, List
from Backend.core.methodology.evaluators.base_evaluator import BaseEvaluator
from Backend.core.methodology.dto.base_candidate import SequenceCandidate
from Backend.core.methodology.dto.base_evaluation import BaseEvaluation, PassedEvaluation, RejectedEvaluation

class SequenceEvaluator(BaseEvaluator):
    """
    Evaluates generic chronological sequences of narrative elements.
    Domain-specific branding (e.g. AMD, Judas Swing) is explicitly omitted here.
    """
    def __init__(self, policy_config: Dict[str, Any] = None):
        self.policy_config = policy_config or {}
        
        self.sequences = self.policy_config.get("sequences", [
            {"pattern": "consolidation-sweep-expansion", "requires": ["consolidation", "sweep", "expansion"]}
        ])
        
    def evaluate(self, candidate: SequenceCandidate, context: Dict[str, Any]) -> BaseEvaluation:
        ordered_types = list(candidate.ordered_elements)
        
        matched_patterns = []
        for seq in self.sequences:
            reqs = seq.get("requires", [])
            req_idx = 0
            
            # Simple chronological greedy matching
            for elem in ordered_types:
                if req_idx < len(reqs) and elem == reqs[req_idx]:
                    req_idx += 1
            
            if req_idx == len(reqs) and len(reqs) > 0:
                matched_patterns.append(seq["pattern"])
                
        if not matched_patterns:
            return RejectedEvaluation(
                evaluator_id="SequenceEvaluator",
                rejected_conditions=["No chronological policy matched the candidate elements"]
            )
            
        return PassedEvaluation(
            evaluator_id="SequenceEvaluator",
            reasons=["Chronological requirements satisfied"],
            metadata={
                "matched_patterns": matched_patterns,
                "event_order": ordered_types,
                "constraints_satisfied": True,
                "coverage": 1.0
            }
        )
