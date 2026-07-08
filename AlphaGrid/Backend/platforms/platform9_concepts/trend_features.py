from typing import Dict, Optional, List
from datetime import datetime, timezone
from Backend.core.state import BaseState
from Backend.platforms.platform9_concepts.feature_base import FeatureType, BooleanFeature, FloatFeature
from Backend.platforms.platform9_concepts.feature_framework import FeaturePlugin
from Backend.platforms.platform9_concepts.feature_registry import feature_registry

class TrendAlignmentFeature(FeaturePlugin):
    @property
    def feature_id(self) -> str:
        return "trend.alignment"
        
    @property
    def required_states(self) -> List[str]:
        return ["trend.moving_average"]
        
    def evaluate(self, states: Dict[str, BaseState]) -> Optional[BooleanFeature]:
        trend_state = states["trend.moving_average"]
        
        return BooleanFeature(
            context=self.context,
            feature_id=self.feature_id,
            feature_value=True, # Stub
            feature_type=FeatureType("trend.alignment", "Trend Alignment", "Trend"),
            version=1,
            quality=1.0,
            confidence=0.9,
            source_states={"trend.moving_average": str(trend_state.version)},
            produced_at=datetime.now(timezone.utc),
            metadata={"description": "Fast MA is above Slow MA."}
        )

feature_registry.register_feature(
    feature_id="trend.alignment",
    feature_class=TrendAlignmentFeature,
    metadata={
        "family": "Trend",
        "consumes_states": ["trend.moving_average"],
        "produces_feature": "Boolean",
        "version": "1.0",
        "description": "True if moving averages are aligned."
    }
)
