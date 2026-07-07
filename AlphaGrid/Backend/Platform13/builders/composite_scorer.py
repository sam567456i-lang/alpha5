from typing import Dict, Any
from Backend.Platform13.contracts.dtos import EvaluatedOpportunityDTO, ConfidenceProvenance
from Backend.Platform13.plugins.base import AbstractBuilderPlugin

class CompositeScoreBuilder(AbstractBuilderPlugin):
    @property
    def plugin_id(self) -> str:
        return "plugin_composite_scorer"

    def build(self, dto: EvaluatedOpportunityDTO, policy: Dict[str, Any]) -> None:
        weights = policy.get("weights", {
            "quality": 0.4,
            "reliability": 0.3,
            "applicability": 0.2,
            "structural_risk_penalty": 0.1
        })
        
        q_score = dto.quality_score * weights.get("quality", 0.4)
        r_score = dto.reliability_score * weights.get("reliability", 0.3)
        a_score = dto.applicability_score * weights.get("applicability", 0.2)
        penalty = dto.structural_risk_score * weights.get("structural_risk_penalty", 0.1)
        
        final_score = max(0.0, min(1.0, (q_score + r_score + a_score) - penalty))
        
        dto.composite_opportunity_score = final_score
        
        dto.confidence_provenance = ConfidenceProvenance(
            opportunity_score=final_score,
            quality_contribution=q_score,
            reliability_contribution=r_score,
            applicability_contribution=a_score,
            portfolio_contribution=0.0,
            competition_contribution=0.0
        )
        
        dto.evaluation_trace[self.plugin_id] = f"Composite score built: {final_score:.2f}"
