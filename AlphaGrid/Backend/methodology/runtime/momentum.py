import hashlib
import uuid
from typing import Dict, Any, List
from Backend.dtos.methodologies import MethodologyDTO
from Backend.dtos.concepts import ConceptDTO

class MomentumRuntimeMethodology:
    """
    Canonical Runtime Momentum Methodology.
    Evaluates the semantic concept structurally to determine market intent.
    Outputs: assessment, confidence, conflicts, support, warnings, required_confirmations.
    No trading logic.
    """
    def __init__(self):
        self.component_id = "meth-momentum-runtime"
        
    def evaluate(self, concepts: List[ConceptDTO], trace_id: str, correlation_id: str) -> MethodologyDTO:
        momentum_concepts = [c for c in concepts if c.concept_type == 'momentum']
        if not momentum_concepts:
            raise ValueError("No momentum concepts provided to methodology.")
            
        # Using the primary concept
        concept = momentum_concepts[0]
        state = concept.state
        concept_meta = concept.metadata
        
        assessment = "NEUTRAL"
        direction = 0
        warnings = []
        required_confirmations = []
        
        # Methodology logic (pure assessment)
        if state in ["ACCELERATING_UP", "STEADY_UP"]:
            assessment = "BULLISH_MOMENTUM"
            direction = 1
            if state == "STEADY_UP":
                warnings.append("Momentum is steady but not accelerating.")
        elif state in ["ACCELERATING_DOWN", "STEADY_DOWN"]:
            assessment = "BEARISH_MOMENTUM"
            direction = -1
            if state == "STEADY_DOWN":
                warnings.append("Momentum is steady but not accelerating.")
        elif state == "DECELERATING_UP":
            assessment = "BULLISH_EXHAUSTION"
            direction = 1
            required_confirmations.append("price_action_reversal")
        elif state == "DECELERATING_DOWN":
            assessment = "BEARISH_EXHAUSTION"
            direction = -1
            required_confirmations.append("price_action_reversal")
        elif state == "DIVERGING":
            assessment = "CONFLICTED"
            direction = 0
            warnings.append("Momentum indicators are in conflict.")
            
        confidence = concept_meta.get("confidence", 0.5)
        quality = concept_meta.get("quality", 0.5)
        
        payload_hash = hashlib.md5(f"{assessment}{direction}{confidence}".encode()).hexdigest()
        
        return MethodologyDTO(
            id=f"{self.component_id}-{uuid.uuid4().hex[:8]}",
            schema_version="1.0.0",
            owner="Methodology",
            producer=self.component_id,
            trace_id=trace_id,
            correlation_id=correlation_id,
            fingerprint="momentum-runtime",
            checksum=payload_hash,
            is_active=True,
            direction=direction,
            metadata={
                "assessment": assessment,
                "confidence": confidence,
                "conflicts": state == "DIVERGING",
                "support": concept_meta.get("supporting_features", []),
                "warnings": warnings,
                "required_confirmations": required_confirmations,
                "quality": quality
            },
            lineage={"dependencies": [concept.producer]}
        )
