from typing import Dict, Any
from Backend.Platform14.contracts.dtos import RecommendationDTO, RecommendationState
from Backend.Platform14.plugins.base import AbstractAnalyzerPlugin

class LifecycleEngine(AbstractAnalyzerPlugin):
    @property
    def plugin_id(self) -> str:
        return "plugin_lifecycle_engine"

    def analyze(self, dto: RecommendationDTO, policy: Dict[str, Any]) -> None:
        """Transitions the lifecycle state of the recommendation."""
        # Simple transition logic based on current state and validation
        if dto.state == RecommendationState.DRAFT:
            dto.state = RecommendationState.GENERATED
            
        if dto.state == RecommendationState.GENERATED:
            if not dto.validation_errors:
                dto.state = RecommendationState.VALIDATED
            else:
                # If there are validation errors, it cannot transition forward
                dto.execution_notes.append("Failed to transition to VALIDATED due to errors.")
                return
                
        # In a real system, APPROVED and READY would involve Platform 15+ or human checks.
        # For P14 completion, if it's validated, we mark it READY for P15.
        if dto.state == RecommendationState.VALIDATED:
            dto.state = RecommendationState.READY
            dto.execution_notes.append("Recommendation is READY for Platform 15.")
