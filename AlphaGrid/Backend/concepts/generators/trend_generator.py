"""Trend Concept Generator."""

from typing import Dict, Any, List
from datetime import datetime
import uuid

from Backend.concepts.base import ConceptGenerator
from Backend.concepts.core.objects import TrendConcept, LifecycleState, ConceptObject


class TrendConceptGenerator(ConceptGenerator):
    """
    Generates semantic TrendConcepts based on Feature Store values.
    This remains completely agnostic of any specific strategy.
    """

    @classmethod
    def get_name(cls) -> str:
        return "TrendConceptGenerator"

    @classmethod
    def get_version(cls) -> str:
        return "v1"

    @classmethod
    def get_dependencies(cls) -> List[str]:
        # Requires EMA features to be present in the feature values
        return ["EMA_20", "EMA_50"]

    def process(self, timestamp: datetime, feature_values: Dict[str, Any], geometry_cache: Any) -> List[ConceptObject]:
        ema_20 = feature_values.get("EMA_20")
        ema_50 = feature_values.get("EMA_50")
        
        if ema_20 is None or ema_50 is None:
            return []

        is_bullish = ema_20 > ema_50
        trend_strength = abs(ema_20 - ema_50) / ema_50 if ema_50 != 0 else 0.0
        
        concept = TrendConcept(
            id=str(uuid.uuid4()),
            version=self.get_version(),
            dataset_id="runtime",
            timeframe="1h",
            timestamp=timestamp,
            concept_type="TREND",
            is_bullish=is_bullish,
            price=float(ema_20),
            trend_strength=float(trend_strength),
            duration_bars=1,
            lifecycle_state=LifecycleState.DETECTED
        )
        
        return [concept]
