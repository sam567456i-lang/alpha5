"""Wyckoff Concept Generator."""

from typing import Any, Dict, List
from datetime import datetime

from Backend.concepts.base import Concept
from Backend.concepts.generator import AbstractConceptGenerator
from Shared.enums.concept_type import ConceptType
from Backend.price_geometry.objects import LifecycleState


class WyckoffConceptGenerator(AbstractConceptGenerator):
    """
    Generates Wyckoff Phase Concepts (Accumulation, Distribution, Mark Up, Mark Down).
    Consumes Geometry Cache for Trading Ranges and Spring events.
    """

    def __init__(self, close_source: str = "close") -> None:
        self.close_src = close_source

    def get_id(self) -> str:
        return "WyckoffPhase"

    def get_version(self) -> str:
        return "v1"

    def get_required_features(self) -> List[str]:
        return [self.close_src]

    def evaluate(self, timestamp: datetime, feature_values: Dict[str, Any], geometry_cache: Any = None) -> Concept:
        price = float(feature_values[self.close_src])
        state = "UNKNOWN"
        confidence = 0.5
        deps = []
        
        if geometry_cache:
            ranges = geometry_cache.get_by_type("Range")
            if ranges:
                latest_range = ranges[-1]
                if getattr(latest_range, 'lifecycle_state', None) == LifecycleState.CONFIRMED:
                    state = "TRADING_RANGE"
                    confidence = 0.7
                    deps.append(latest_range.id)

        concept_type = getattr(ConceptType, 'MARKET_STRUCTURE', ConceptType.UNKNOWN)

        return Concept(
            id=f"{self.get_id()}_{state}",
            type=concept_type,
            version=self.get_version(),
            timestamp=timestamp,
            confidence=confidence,
            inputs={"price": price, "state": state},
            generator=self.__class__.__name__,
            geometry_dependencies=deps
        )
