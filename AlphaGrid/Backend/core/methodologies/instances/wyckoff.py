from typing import List
from Backend.core.methodologies.core_models import MethodologyInstance, MethodologyContext
from Backend.core.methodologies.evidence import MethodologyClaim, ClaimCategory, ConfidenceVector, ExplanationObject

class WyckoffMethodology(MethodologyInstance):
    def evaluate(self, context: MethodologyContext) -> List[MethodologyClaim]:
        """
        Wyckoff Implementation.
        Requires Volume, Momentum, Price Action.
        """
        claims = []
        
        # Mock Evidence
        has_volume_climax = True
        has_spring = True
        
        if has_volume_climax and has_spring:
            vec = ConfidenceVector(0.8, context.data_quality_score, 0.9, 0.8, 1.0, 0.85)
            exp = ExplanationObject("WyckoffSpring", "SPRING_UUID", "HIGH", ["CLIMAX_UUID"], 1.0)
            
            claim = MethodologyClaim(
                claim_id="clm_wyckoff_001",
                claim_type="PhaseC_Spring",
                category=ClaimCategory.STRUCTURAL,
                confidence_vector=vec,
                valid_until_bar=15,
                invalidation_conditions=["NEW_LOW_HIGH_VOLUME"],
                evidence_trace=["CLIMAX_UUID", "SPRING_UUID"],
                explanation_objects=[exp],
                methodology_version=self.version.version_id,
                context_id=context.context_id
            )
            claims.append(claim)
            
        return claims
