import hashlib
import uuid
from typing import List
from Backend.dtos.concepts import ConceptDTO
from Backend.dtos.features import FeatureDTO

class ExtremumConceptGenerator:
    def __init__(self, overbought_threshold: float, oversold_threshold: float, feature_key: str):
        self.overbought = overbought_threshold
        self.oversold = oversold_threshold
        self.feature_key = feature_key
        self.component_id = f"con-extremum-{feature_key}"
        
    def generate(self, feature: FeatureDTO, trace_id: str, correlation_id: str) -> ConceptDTO:
        if self.feature_key not in feature.values:
            raise ValueError(f"FeatureDTO does not contain required key '{self.feature_key}'")
            
        value = feature.values[self.feature_key]
        
        state = "NEUTRAL"
        if value >= self.overbought:
            state = "OVERBOUGHT"
        elif value <= self.oversold:
            state = "OVERSOLD"
            
        payload = f"{self.feature_key}:{state}:{value}"
        payload_hash = hashlib.md5(payload.encode()).hexdigest()
        
        return ConceptDTO(
            id=f"{self.component_id}-{uuid.uuid4().hex[:8]}",
            schema_version="2.0.0",
            producer=self.component_id,
            trace_id=trace_id,
            correlation_id=correlation_id,
            fingerprint=f"extremum-{self.feature_key}",
            checksum=payload_hash,
            concept_type="EXTREMUM",
            state=state,
            metadata={"strength": abs(value - ((self.overbought + self.oversold)/2)), "current_value": value},
            lineage={'dependencies': [feature.id]}
        )
