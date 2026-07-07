from typing import Dict, Any
from Backend.Platform14.contracts.dtos import RecommendationDTO, RecommendationState
from Backend.Platform14.plugins.base import AbstractBuilderPlugin

class RecommendationBuilder(AbstractBuilderPlugin):
    @property
    def plugin_id(self) -> str:
        return "plugin_recommendation_builder"

    def build(self, dto: RecommendationDTO, policy: Dict[str, Any]) -> None:
        # Check if validation passed
        if dto.state != RecommendationState.READY:
            dto.execution_notes.append("Recommendation Builder: DTO is not in READY state. Builder aborted.")
            return
            
        # Finalize the DTO
        if dto.evaluated_opportunity and hasattr(dto.evaluated_opportunity, "composite_opportunity_score"):
            dto.confidence = dto.evaluated_opportunity.composite_opportunity_score
            
        dto.execution_notes.append("Recommendation finalized.")
        
        # Provenance Hashes (Rule 10 - Full Trace Cryptographic Hash)
        dto.compute_hashes()

