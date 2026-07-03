import hashlib
import uuid
from typing import List
from Backend.dtos.concepts import ConceptDTO
from Backend.dtos.features import FeatureDTO


class BreakoutConceptGenerator:
    """Generic semantic concept that maps any breakout feature into
    BREAKOUT_BULLISH, BREAKOUT_BEARISH, or CONTAINED states.

    Consumes any feature that produces boolean breakout flags
    (high_breakout/low_breakout, upside_breakout/downside_breakout)
    or distance-based proximity signals (distance_to_resistance/distance_to_support).
    """

    component_metadata = {
        'consumes': ['FeatureDTO'],
        'produces': ['ConceptDTO'],
        'deterministic': True,
        'switch': 'breakout_family',
    }

    def __init__(self, proximity_threshold: float = 0.05):
        self.proximity_threshold = proximity_threshold
        self.component_id = "con-breakout"

    def generate(self, features: List[FeatureDTO], trace_id: str, correlation_id: str) -> ConceptDTO:
        bullish_signals = 0
        bearish_signals = 0

        for f in features:
            vals = f.values
            # Boolean breakout flags
            if vals.get('high_breakout') or vals.get('upside_breakout'):
                bullish_signals += 1
            if vals.get('low_breakout') or vals.get('downside_breakout'):
                bearish_signals += 1
            # Proximity-based signals (S/R)
            dist_res = vals.get('distance_to_resistance')
            if dist_res is not None and dist_res <= self.proximity_threshold:
                bullish_signals += 1
            dist_sup = vals.get('distance_to_support')
            if dist_sup is not None and dist_sup <= self.proximity_threshold:
                bearish_signals += 1

        if bullish_signals > bearish_signals:
            state = "BREAKOUT_BULLISH"
        elif bearish_signals > bullish_signals:
            state = "BREAKOUT_BEARISH"
        else:
            state = "CONTAINED"

        payload = f"{state}:{bullish_signals}:{bearish_signals}"
        payload_hash = hashlib.md5(payload.encode()).hexdigest()

        return ConceptDTO(
            id=f"{self.component_id}-{uuid.uuid4().hex[:8]}",
            schema_version="1.0.0",
            producer=self.component_id,
            trace_id=trace_id,
            correlation_id=correlation_id,
            fingerprint="breakout-concept",
            checksum=payload_hash,
            concept_type="BREAKOUT",
            state=state,
            metadata={
                'bullish_signals': bullish_signals,
                'bearish_signals': bearish_signals,
            },
            lineage={'dependencies': [f.id for f in features]}
        )
