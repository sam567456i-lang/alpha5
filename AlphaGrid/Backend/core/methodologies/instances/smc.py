from typing import List
from Backend.core.methodologies.core_models import MethodologyInstance, MethodologyContext
from Backend.core.methodologies.evidence import MethodologyClaim, ClaimCategory, ConfidenceVector, ExplanationObject

class SMCMethodology(MethodologyInstance):
    def evaluate(self, context: MethodologyContext) -> List[MethodologyClaim]:
        """
        SMC Profile Implementation.
        Requires Liquidity, Structure, Imbalance.
        """
        claims = []
        
        # 1. Evidence Extraction
        # In a real environment, this extracts specific UUIDs from the object_graph_snapshot
        has_liquidity_sweep = True # Mock
        has_bos = True # Mock
        has_fvg = True # Mock
        
        # 2. Synthesis Logic
        if has_liquidity_sweep and has_bos and has_fvg:
            # 3. Claim Generation
            vec = ConfidenceVector(0.9, context.data_quality_score, 1.0, 0.95, 1.0, 0.9)
            exp = ExplanationObject("StructuralBreak", "BOS_UUID", "HIGH", ["SWEEP_UUID"], 1.0)
            
            claim = MethodologyClaim(
                claim_id="clm_smc_001",
                claim_type="ChangeOfCharacter",
                category=ClaimCategory.STRUCTURAL,
                confidence_vector=vec,
                valid_until_bar=20,
                invalidation_conditions=["BOS_OPPOSITE", "LIQUIDITY_SWEEP_OPPOSITE"],
                evidence_trace=["SWEEP_UUID", "BOS_UUID", "FVG_UUID"],
                explanation_objects=[exp],
                methodology_version=self.version.version_id,
                context_id=context.context_id
            )
            claims.append(claim)
            
        return claims
