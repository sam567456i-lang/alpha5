from typing import List, Dict, Any
from Backend.core.interfaces.methodology_consensus_dto import MethodologyConsensusDTO

class MethodologyConsensusEngine:
    """
    Consumes methodologies and their conflicts to produce the unified Probability Matrix.
    """
    def generate_consensus(self, assessments: List[Dict[str, Any]], conflicts: List[Dict[str, Any]]) -> MethodologyConsensusDTO:
        dominant = []
        unresolved = [c for c in conflicts] # Simplification for scaffold
        
        # Super basic counting for probability distribution scaffold
        bias_counts = {}
        for a in assessments:
            b = a.get("semantic_bias")
            if b:
                bias_counts[b] = bias_counts.get(b, 0) + 1
                
        total = sum(bias_counts.values())
        probabilities = {k: v/total for k, v in bias_counts.items()} if total > 0 else {}
        
        # If one bias is > 50%, mark it dominant
        for b, p in probabilities.items():
            if p > 0.5:
                dominant.append(b)
                
        # High uncertainty if no bias > 50%
        uncertainty = 1.0 - max(probabilities.values()) if probabilities else 1.0
        
        return MethodologyConsensusDTO(
            dominant_hypotheses=dominant,
            agreement_clusters=bias_counts, # Simplified
            unresolved_conflicts=[str(c) for c in unresolved],
            probabilities=probabilities,
            uncertainty_score=uncertainty,
            active_methodology_count=len(assessments)
        )
