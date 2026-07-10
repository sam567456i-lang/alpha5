from typing import Dict, Any, List, Tuple
from Backend.core.methodology.evaluators.base_evaluator import BaseEvaluator
from Backend.core.methodology.dto.base_candidate import LiquidityCandidate, CandidateIdentity
from Backend.core.methodology.dto.base_evaluation import BaseEvaluation, PassedEvaluation
from Backend.core.methodology.dto.base_interpretation import TargetInterpretation
from Backend.core.methodology.multi_timeframe_graph import MultiTimeframeEvidenceGraph

class LiquidityEvaluator(BaseEvaluator):
    """
    Evaluates Liquidity Candidates and yields PassedEvaluations which map into TargetInterpretations.
    Matches the legacy ICTLiquidityModule.
    """
    def __init__(self):
        pass

    def evaluate(self, candidate: LiquidityCandidate, context: Dict[str, Any]) -> BaseEvaluation:
        # In the new framework, Candidates are evaluated one by one.
        # So we receive a LiquidityCandidate and rank/score it.
        
        # We need to replicate the exact scoring logic.
        tf = candidate.metadata.get("tf", "")
        pool_type = candidate.metadata.get("type", "")
        
        ranking_components = {
            "structure_alignment": 0,
            "htf_alignment": 0,
            "liquidity_size": 15,
            "distance": 10
        }
        
        if tf == "1D":
            ranking_components["htf_alignment"] = 30
        elif tf == "4H":
            ranking_components["htf_alignment"] = 20
            
        if pool_type in ["BSL", "EQH"]:
            ranking_components["structure_alignment"] = 30
            
        score = sum(ranking_components.values())
        
        # Legacy module always creates a TargetNode from the CandidateNode. 
        # So we always return PassedEvaluation.
        # We attach the score to the reasons/metadata for downstream interpretation.
        return PassedEvaluation(
            evaluator_id="LiquidityEvaluator",
            reasons=[f"Liquidity pool validated with score {score}"]
        )
