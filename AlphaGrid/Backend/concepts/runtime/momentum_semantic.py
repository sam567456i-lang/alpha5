import hashlib
import uuid
from typing import Dict, Any, List
from Backend.dtos.concepts import ConceptDTO
from Backend.dtos.features import FeatureDTO

class MomentumSemanticConceptGenerator:
    """
    Canonical Runtime Momentum Semantic Concept.
    Indicator-agnostic. Evaluates generic momentum semantics.
    """
    def __init__(self):
        self.component_id = "con-momentum-semantic"
        
    def evaluate(self, features: List[FeatureDTO], trace_id: str, correlation_id: str) -> ConceptDTO:
        # Filter for features that expose momentum semantics
        momentum_features = [f for f in features if f.metadata.get('feature_type') == 'momentum']
        if not momentum_features:
            raise ValueError("No momentum features provided to concept.")
            
        # Aggregate semantics (in a real system, you'd apply weightings)
        avg_strength = sum(f.values.get('momentum_strength', 0.0) for f in momentum_features) / len(momentum_features)
        avg_acceleration = sum(f.values.get('momentum_acceleration', 0.0) for f in momentum_features) / len(momentum_features)
        directions = [f.values.get('momentum_direction', 0.0) for f in momentum_features]
        
        # State Machine Logic
        state = "NEUTRAL"
        if all(d > 0 for d in directions):
            if avg_acceleration > 0:
                state = "ACCELERATING_UP"
            elif avg_acceleration < 0:
                state = "DECELERATING_UP"
            else:
                state = "STEADY_UP"
        elif all(d < 0 for d in directions):
            if avg_acceleration < 0:
                state = "ACCELERATING_DOWN"
            elif avg_acceleration > 0:
                state = "DECELERATING_DOWN"
            else:
                state = "STEADY_DOWN"
        else:
            state = "DIVERGING" # Conflict among features
            
        # Quality & Confidence
        confidence = 0.9 if state != "DIVERGING" else 0.5
        quality = 1.0
        stability = "HIGH" if abs(avg_acceleration) < 1.0 else "LOW" # arbitrary heuristic
        supporting_features = [f.producer for f in momentum_features]
        
        payload_hash = hashlib.md5(f"{state}{confidence}{avg_strength}".encode()).hexdigest()
        
        return ConceptDTO(
            id=f"{self.component_id}-{uuid.uuid4().hex[:8]}",
            schema_version="1.0.0",
            owner="Concept",
            producer=self.component_id,
            trace_id=trace_id,
            correlation_id=correlation_id,
            fingerprint="momentum-semantic",
            checksum=payload_hash,
            concept_type="momentum",
            state=state,
            metadata={
                "confidence": confidence,
                "quality": quality,
                "stability": stability,
                "supporting_features": supporting_features,
                "aggregate_strength": avg_strength,
                "aggregate_acceleration": avg_acceleration
            },
            lineage={"dependencies": supporting_features}
        )
