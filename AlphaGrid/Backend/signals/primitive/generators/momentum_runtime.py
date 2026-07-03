import hashlib
import uuid
from typing import Dict, Any, List
from Backend.dtos.signals import SignalDTO
from Backend.dtos.methodologies import MethodologyDTO

class MomentumRuntimeSignalGenerator:
    """
    Canonical Runtime Momentum Signal Generator.
    Produces atomic, execution-agnostic intent signals.
    Payload: signal_type, confidence, priority, expiration, dependencies, invalidated_by.
    """
    def __init__(self):
        self.component_id = "sig-momentum-runtime"
        
    def generate(self, methodologies: List[MethodologyDTO], trace_id: str, correlation_id: str) -> SignalDTO:
        momentum_meths = [m for m in methodologies if 'momentum' in m.producer.lower()]
        if not momentum_meths:
            raise ValueError("No momentum methodologies provided to signal generator.")
            
        meth = momentum_meths[0]
        assessment = meth.metadata.get("assessment", "NEUTRAL")
        direction = meth.direction
        
        signal_type = "NEUTRAL"
        priority = "LOW"
        expiration = 5 # arbitrary default expiration in bars
        invalidated_by = []
        
        if assessment == "BULLISH_MOMENTUM":
            signal_type = "ENTRY_READY"
            priority = "HIGH"
            invalidated_by = ["BEARISH_MOMENTUM", "BULLISH_EXHAUSTION"]
        elif assessment == "BEARISH_MOMENTUM":
            signal_type = "ENTRY_READY"
            priority = "HIGH"
            invalidated_by = ["BULLISH_MOMENTUM", "BEARISH_EXHAUSTION"]
        elif assessment == "BULLISH_EXHAUSTION":
            signal_type = "WEAKENING"
            priority = "MEDIUM"
            invalidated_by = ["BULLISH_MOMENTUM"]
        elif assessment == "BEARISH_EXHAUSTION":
            signal_type = "WEAKENING"
            priority = "MEDIUM"
            invalidated_by = ["BEARISH_MOMENTUM"]
        elif assessment == "CONFLICTED":
            signal_type = "CONFLICT"
            priority = "HIGH"
            expiration = 1
            
        confidence = meth.metadata.get("confidence", 0.5)
        
        payload_hash = hashlib.md5(f"{signal_type}{direction}{confidence}".encode()).hexdigest()
        
        return SignalDTO(
            id=f"{self.component_id}-{uuid.uuid4().hex[:8]}",
            schema_version="1.0.0",
            owner="Signal",
            producer=self.component_id,
            trace_id=trace_id,
            correlation_id=correlation_id,
            fingerprint="momentum-runtime-signal",
            checksum=payload_hash,
            direction=direction,
            signal_type=signal_type,
            metadata={
                "confidence": confidence,
                "priority": priority,
                "expiration": expiration,
                "dependencies": meth.metadata.get("support", []),
                "invalidated_by": invalidated_by
            },
            lineage={"dependencies": [meth.producer]}
        )
