import hashlib
import uuid
from typing import List, Optional
from Backend.dtos.methodologies import MethodologyDTO
from Backend.dtos.concepts import ConceptDTO


class BreakoutMethodology:
    """Evaluates semantic concepts to determine whether a breakout setup is actionable.

    Never references specific indicator thresholds. Instead it evaluates:
    - BreakoutConcept state (BREAKOUT_BULLISH/BREAKOUT_BEARISH/CONTAINED)
    - TrendConcept alignment (optional - confirms direction)
    - VolatilityConcept expansion (optional - confirms energy)
    """

    component_metadata = {
        'consumes': ['ConceptDTO'],
        'produces': ['MethodologyDTO'],
        'dependencies': {
            'required': ['BreakoutConcept'],
            'optional': ['TrendConcept', 'VolatilityConcept']
        },
        'deterministic': True,
        'switch': 'breakout_family',
    }

    def __init__(self):
        self.component_id = "meth-breakout"

    def evaluate(
        self,
        breakout_concept: ConceptDTO,
        trend_concept: Optional[ConceptDTO] = None,
        volatility_concept: Optional[ConceptDTO] = None,
        trace_id: str = "",
        correlation_id: str = "",
    ) -> MethodologyDTO:
        direction = 0
        active = False

        if breakout_concept.state == "BREAKOUT_BULLISH":
            direction = 1
            active = True
        elif breakout_concept.state == "BREAKOUT_BEARISH":
            direction = -1
            active = True

        # Trend confirmation strengthens conviction but doesn't change direction
        trend_aligned = False
        if trend_concept:
            if direction == 1 and trend_concept.state == "BULLISH":
                trend_aligned = True
            elif direction == -1 and trend_concept.state == "BEARISH":
                trend_aligned = True

        payload = f"{direction}:{active}:{trend_aligned}"
        payload_hash = hashlib.md5(payload.encode()).hexdigest()

        dependencies = [breakout_concept.id]
        if trend_concept:
            dependencies.append(trend_concept.id)
        if volatility_concept:
            dependencies.append(volatility_concept.id)

        return MethodologyDTO(
            id=f"{self.component_id}-{uuid.uuid4().hex[:8]}",
            schema_version="1.0.0",
            producer=self.component_id,
            trace_id=trace_id,
            correlation_id=correlation_id,
            fingerprint="breakout-methodology",
            checksum=payload_hash,
            is_active=active,
            direction=direction,
            metadata={
                'trend_aligned': trend_aligned,
                'breakout_state': breakout_concept.state,
            },
            lineage={'dependencies': dependencies}
        )
