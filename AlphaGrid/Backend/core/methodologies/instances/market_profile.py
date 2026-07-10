from typing import List
from Backend.core.methodologies.core_models import MethodologyInstance, MethodologyContext
from Backend.core.methodologies.evidence import MethodologyClaim, ClaimCategory, ConfidenceVector, ExplanationObject

class MarketProfileMethodology(MethodologyInstance):
    def evaluate(self, context: MethodologyContext) -> List[MethodologyClaim]:
        """
        Market Profile / AMT Implementation.
        Requires Market Profile, Volume Profile, AMT.
        """
        claims = []
        
        # Mock Evidence
        is_open_drive = True
        value_area_acceptance = True
        
        if is_open_drive and value_area_acceptance:
            vec = ConfidenceVector(0.75, context.data_quality_score, 1.0, 0.9, 1.0, 0.9)
            exp = ExplanationObject("AMTAcceptance", "VA_UUID", "MEDIUM", ["OPEN_DRIVE_UUID"], 1.0)
            
            claim = MethodologyClaim(
                claim_id="clm_mp_001",
                claim_type="ValueAreaAcceptance",
                category=ClaimCategory.DIRECTIONAL,
                confidence_vector=vec,
                valid_until_bar=5,
                invalidation_conditions=["REJECTION_SPIKE"],
                evidence_trace=["OPEN_DRIVE_UUID", "VA_UUID"],
                explanation_objects=[exp],
                methodology_version=self.version.version_id,
                context_id=context.context_id
            )
            claims.append(claim)
            
        return claims
