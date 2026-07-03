import hashlib
import uuid
from typing import List
from Backend.dtos.signals import SignalDTO
from Backend.dtos.methodologies import MethodologyDTO

class ExtremumReversionPrimitiveSignalGenerator:
    def __init__(self):
        self.component_id = "sig-gen-extremumreversion"
        
    def generate(self, methodology: MethodologyDTO, trace_id: str, correlation_id: str) -> SignalDTO:
        if methodology.producer != "meth-meanreversion":
            raise ValueError("Invalid Methodology for Reversion Primitive Signal")
            
        signal_type = "MEAN_REVERSION_CANCEL"
        direction = 0
        
        if methodology.is_active:
            direction = methodology.direction
            if direction == 1:
                signal_type = "MEAN_REVERSION_LONG"
            elif direction == -1:
                signal_type = "MEAN_REVERSION_SHORT"
                
        payload = f"{direction}:{signal_type}"
        payload_hash = hashlib.md5(payload.encode()).hexdigest()
        
        return SignalDTO(
            id=f"{self.component_id}-{uuid.uuid4().hex[:8]}",
            schema_version="1.0.0",
            producer=self.component_id,
            trace_id=trace_id,
            correlation_id=correlation_id,
            fingerprint="sig-meanreversion",
            checksum=payload_hash,
            direction=direction,
            signal_type=signal_type,
            lineage={'dependencies': [methodology.id]}
        )
