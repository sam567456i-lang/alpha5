from typing import List, Dict, Any, Optional
from Backend.core.methodology.dto.base_interpretation import BaseInterpretation

class ExplanationTraversalEngine:
    """
    A traversal engine that queries the EvidenceGraph and InterpretationGraph to explain 'why'.
    Supports partial depths (Candidate only, Evaluation only, Full chain).
    """
    
    def __init__(self, interpretation_registry: Any, evidence_graph: Any):
        self.interpretation_registry = interpretation_registry
        self.evidence_graph = evidence_graph
        
    def trace_lineage(self, interpretation_id: str, depth: str = "FULL") -> Dict[str, Any]:
        """
        Depth options: "INTERPRETATION", "CANDIDATE", "EVALUATION", "FULL"
        """
        interp: BaseInterpretation = self.interpretation_registry.get(interpretation_id)
        if not interp:
            return {"error": "Interpretation not found."}
            
        lineage = {
            "interpretation_id": interp.identity.id,
            "methodology": interp.identity.methodology_id,
            "profile": interp.identity.profile_id,
        }
        
        if depth == "INTERPRETATION":
            return lineage
            
        lineage["evaluation_id"] = interp.identity.evaluation_id
        lineage["candidate_id"] = interp.identity.candidate_id
        
        if depth in ["CANDIDATE", "EVALUATION"]:
            return lineage
            
        # FULL: traverse to evidence
        # Dummy mock traversal for now
        lineage["evidence_lineage"] = [
            {"evidence_id": "ev_123", "type": "PoolState"},
            {"evidence_id": "ev_456", "type": "SweepEvent"}
        ]
        
        return lineage
