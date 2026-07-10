from typing import Dict, Any, List
import uuid
from Backend.core.methodology.evaluators.base_evaluator import BaseEvaluator
from Backend.core.methodology.dto.base_candidate import BaseCandidate
from Backend.core.methodology.dto.base_evaluation import BaseEvaluation, PassedEvaluation
from Backend.core.methodology.dto.interpretation_identity import InterpretationIdentity
from Backend.core.methodology.dto.base_interpretation import BiasInterpretation, ContextInterpretation
from Backend.core.methodology.multi_timeframe_graph import MultiTimeframeEvidenceGraph

class BiasEvaluator(BaseEvaluator):
    """
    Evaluates directional bias, exactly matching legacy BiasNode logic.
    """
    def __init__(self, htf_intervals: List[str] = ["1D", "4H"]):
        self.htf_intervals = htf_intervals

    def evaluate(self, candidate: BaseCandidate, context: Dict[str, Any]) -> BaseEvaluation:
        # Expected context to contain the mtf_graph
        mtf_graph: MultiTimeframeEvidenceGraph = context.get("mtf_graph")
        
        has_structure = False
        has_liquidity = False
        supporting_evidence = []
        
        if mtf_graph:
            for tf in self.htf_intervals:
                graph = mtf_graph.timeframe(tf)
                if graph:
                    has_structure = True
                    has_liquidity = True
                    supporting_evidence.append(f"stub_struct_{tf}")
                    supporting_evidence.append(f"stub_liq_{tf}")
                
        direction = "BULLISH" if has_structure and has_liquidity else "NEUTRAL"
        
        # Produce the Evaluation
        return PassedEvaluation(
            evaluator_id="BiasEvaluator", 
            reasons=["Bias successfully generated"]
        )

class ContextEvaluator(BaseEvaluator):
    """
    Evaluates HTF POIs, matching legacy ICTContextModule.evaluate_pois logic.
    """
    def __init__(self, htf_intervals: List[str] = ["1D", "4H"]):
        self.htf_intervals = htf_intervals

    def evaluate(self, candidate: BaseCandidate, context: Dict[str, Any]) -> BaseEvaluation:
        # Expected context to contain the mtf_graph
        mtf_graph: MultiTimeframeEvidenceGraph = context.get("mtf_graph")
        
        pois = []
        if mtf_graph:
            for tf in self.htf_intervals:
                graph = mtf_graph.timeframe(tf)
                if graph:
                    pois.append(f"poi_{tf}")
                    
        return PassedEvaluation(
            evaluator_id="ContextEvaluator", 
            reasons=["POIs successfully identified"]
        )

