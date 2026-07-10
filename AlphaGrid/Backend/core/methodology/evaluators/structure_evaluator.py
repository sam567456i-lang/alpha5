from typing import Dict, Any, List
from Backend.core.methodology.evaluators.base_evaluator import BaseEvaluator
from Backend.core.methodology.dto.base_candidate import StructureCandidate
from Backend.core.methodology.dto.base_evaluation import BaseEvaluation, PassedEvaluation, RejectedEvaluation

class StructureEvaluator(BaseEvaluator):
    """
    Evaluates StructureCandidates against methodology-specific structure policies.
    Migrated from ICTStructureModule.
    """
    def __init__(self, policy_config: Dict[str, Any] = None):
        self.policy_config = policy_config or {}

    def evaluate(self, candidate: StructureCandidate, context: Dict[str, Any]) -> BaseEvaluation:
        proposed_label = candidate.structure_type
        metadata = candidate.metadata
        
        approved = False
        reasons = []
        
        if proposed_label == "BOS":
            req_align = self.policy_config.get("bos_requires_context_alignment", True)
            aligned = metadata.get("alignment_with_context", False)
            if req_align and not aligned:
                reasons.append("Failed BOS Context Alignment")
            else:
                approved = True
                
        elif proposed_label == "CHOCH":
            req_mit = self.policy_config.get("choch_requires_poi_mitigation", True)
            mitigated = metadata.get("poi_mitigated", False)
            if req_mit and not mitigated:
                reasons.append("Failed CHOCH POI Mitigation")
            else:
                approved = True
                
        elif proposed_label == "MSS":
            req_sweep = self.policy_config.get("mss_requires_htf_liquidity_sweep", True)
            req_disp = self.policy_config.get("mss_requires_displacement", True)
            req_mtf = self.policy_config.get("mss_requires_multi_timeframe_confirmation", True)
            
            has_sweep = metadata.get("swept_liquidity", False)
            has_disp = metadata.get("has_displacement", False)
            mtf_conf = metadata.get("is_multi_timeframe_confirmed", False)
            
            approved = True
            if req_sweep and not has_sweep:
                approved = False
                reasons.append("Missing HTF Liquidity Sweep")
            if req_disp and not has_disp:
                approved = False
                reasons.append("Missing Displacement")
            if req_mtf and not mtf_conf:
                approved = False
                reasons.append("Missing MTF Confirmation")
                
        else:
            reasons.append(f"Unknown structure type: {proposed_label}")
            
        if approved:
            return PassedEvaluation(
                evaluator_id="StructureEvaluator",
                reasons=[f"{proposed_label} structure verified"]
            )
        else:
            return RejectedEvaluation(
                evaluator_id="StructureEvaluator",
                reasons=reasons
            )
