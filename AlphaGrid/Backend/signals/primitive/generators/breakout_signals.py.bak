import hashlib
import uuid
from Backend.dtos.signals import SignalDTO
from Backend.dtos.methodologies import MethodologyDTO


class BreakoutPrimitiveSignalGenerator:
    """Generates rich breakout signals from BreakoutMethodology output."""

    component_metadata = {
        'consumes': ['MethodologyDTO'],
        'produces': ['SignalDTO'],
        'deterministic': True,
        'switch': 'breakout_family',
    }

    def __init__(self):
        self.component_id = "sig-gen-breakout"

    def generate(self, methodology: MethodologyDTO, trace_id: str, correlation_id: str) -> SignalDTO:
        signal_type = "BREAKOUT_CANCEL"
        direction = 0
        confidence = 0.0

        if methodology.is_active:
            direction = methodology.direction
            trend_aligned = methodology.metadata.get('trend_aligned', False)

            if direction == 1:
                signal_type = "BREAKOUT_LONG_CONFIRMED" if trend_aligned else "BREAKOUT_LONG"
            elif direction == -1:
                signal_type = "BREAKOUT_SHORT_CONFIRMED" if trend_aligned else "BREAKOUT_SHORT"

            # Confidence: confirmed breakouts receive higher confidence
            confidence = 0.85 if trend_aligned else 0.60

        payload = f"{direction}:{signal_type}:{confidence}"
        payload_hash = hashlib.md5(payload.encode()).hexdigest()

        return SignalDTO(
            id=f"{self.component_id}-{uuid.uuid4().hex[:8]}",
            schema_version="1.0.0",
            producer=self.component_id,
            trace_id=trace_id,
            correlation_id=correlation_id,
            fingerprint="sig-breakout",
            checksum=payload_hash,
            confidence=confidence,
            direction=direction,
            signal_type=signal_type,
            lineage={'dependencies': [methodology.id]}
        )

