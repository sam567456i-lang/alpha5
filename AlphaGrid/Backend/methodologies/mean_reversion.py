import hashlib
import uuid
from typing import List, Optional
from Backend.dtos.methodologies import MethodologyDTO
from Backend.dtos.concepts import ConceptDTO

class MeanReversionMethodology:
    def __init__(self):
        self.component_id = "meth-meanreversion"
        
    def evaluate(self, extremum_concepts: List[ConceptDTO], volatility_concept: Optional[ConceptDTO], trace_id: str, correlation_id: str) -> MethodologyDTO:
        direction = 0
        active = False
        
        overbought_count = sum(1 for c in extremum_concepts if c.state == 'OVERBOUGHT')
        oversold_count = sum(1 for c in extremum_concepts if c.state == 'OVERSOLD')
        
        # Methodology logic: if multiple oscillators agree, trigger reversion setup
        if overbought_count > oversold_count:
            direction = -1 # Setup for short
            active = True
        elif oversold_count > overbought_count:
            direction = 1 # Setup for long
            active = True
            
        payload = f"{direction}:{active}:{overbought_count}:{oversold_count}"
        payload_hash = hashlib.md5(payload.encode()).hexdigest()
        
        dependencies = [c.id for c in extremum_concepts]
        if volatility_concept:
            dependencies.append(volatility_concept.id)
            
        return MethodologyDTO(
            id=f"{self.component_id}-{uuid.uuid4().hex[:8]}",
            schema_version="1.0.0",
            producer=self.component_id,
            trace_id=trace_id,
            correlation_id=correlation_id,
            fingerprint="meanreversion-methodology",
            checksum=payload_hash,
            is_active=active,
            direction=direction,
            metadata={"overbought_sources": overbought_count, "oversold_sources": oversold_count},
            lineage={'dependencies': dependencies}
        )
