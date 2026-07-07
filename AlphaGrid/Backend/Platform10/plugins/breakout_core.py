import hashlib
import uuid
from typing import Optional
from Backend.dtos.concepts import ConceptDTO
from Backend.Platform10.contracts.dtos import MethodologyProfileDTO, ExplainabilityDTO

class BreakoutCoreMethodology:
    """Breakout Methodology Implementation for Platform 10.
    
    Migrates the semantic evaluation from the legacy BreakoutMethodology.
    Evaluates:
    - BreakoutConcept state (BREAKOUT_BULLISH/BREAKOUT_BEARISH)
    - TrendConcept alignment (optional - strengthens persistence/confidence)
    - VolatilityConcept expansion (optional - strengthens velocity)
    """
    
    def __init__(self):
        self.component_id = "cap_meth_breakout_core"
        
    def evaluate(
        self,
        breakout_concept: ConceptDTO,
        trend_concept: Optional[ConceptDTO] = None,
        volatility_concept: Optional[ConceptDTO] = None,
        execution_context=None,
    ) -> MethodologyProfileDTO:
        direction = 0
        active = False
        
        # 1. Behavior Equivalence: Breakout detection logic
        if breakout_concept.state == "BREAKOUT_BULLISH":
            direction = 1
            active = True
        elif breakout_concept.state == "BREAKOUT_BEARISH":
            direction = -1
            active = True
            
        # 2. Behavior Equivalence: Trend alignment
        trend_aligned = False
        if trend_concept:
            if direction == 1 and trend_concept.state == "BULLISH":
                trend_aligned = True
            elif direction == -1 and trend_concept.state == "BEARISH":
                trend_aligned = True
                
        # 3. Behavior Equivalence: Volatility alignment (Legacy checked it as a dependency)
        volatility_aligned = False
        if volatility_concept and active:
            # Assuming if it was passed, it signifies an expansion supportive of breakout
            volatility_aligned = True
            
        # DTO Construction (Platform 10 additions)
        confidence = 0.5 if active else 0.0
        applicability = 0.5 if active else 0.0
        
        if trend_aligned:
            confidence += 0.2
            applicability += 0.2
        if volatility_aligned:
            confidence += 0.2
            applicability += 0.2
            
        # Bound scores
        confidence = min(1.0, confidence)
        applicability = min(1.0, applicability)
        
        dependencies = [breakout_concept.id]
        if trend_concept:
            dependencies.append(trend_concept.id)
        if volatility_concept:
            dependencies.append(volatility_concept.id)
            
        payload = f"{direction}:{active}:{trend_aligned}:{volatility_aligned}"
        payload_hash = hashlib.md5(payload.encode()).hexdigest()
        
        explainability = ExplainabilityDTO(
            rationale="Breakout state detected." if active else "No breakout detected.",
            supporting_evidence=dependencies,
            conflicting_evidence=[],
            regime_compatibility=["Trending", "Volatile"]
        )
        
        return MethodologyProfileDTO(
            id=f"{self.component_id}-{uuid.uuid4().hex[:8]}",
            schema_version="2.0.0",
            owner="Platform10",
            producer=self.component_id,
            execution_context=execution_context,
            fingerprint="breakout-core-v1",
            checksum=payload_hash,
            
            is_active=active,
            direction=direction,
            strength="Strong" if confidence >= 0.8 else ("Moderate" if confidence >= 0.5 else "Weak"),
            quality="Good" if trend_aligned else "Fair",
            persistence="Medium",
            maturity="Emerging",
            
            # Base constraints
            confidence=confidence,
            reliability=confidence * 0.9,
            applicability=applicability,
            provenance="BreakoutCoreMethodology",
            explainability=explainability,
            lineage={'dependencies': dependencies}
        )
