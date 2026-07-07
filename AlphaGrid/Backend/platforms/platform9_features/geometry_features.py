from typing import Dict, Optional, List
from datetime import datetime, timezone
from Backend.core.state import BaseState
from Backend.platforms.platform9_features.feature_base import FeatureType, BooleanFeature, FloatFeature
from Backend.platforms.platform9_features.feature_framework import FeaturePlugin
from Backend.platforms.platform9_features.feature_registry import feature_registry

class RangeBreakoutFeature(FeaturePlugin):
    """
    Evaluates if price broke out of a range.
    Depends on Geometry's RangeState and TimeExtremesState.
    """
    @property
    def feature_id(self) -> str:
        return "geometry.range_breakout"
        
    @property
    def required_states(self) -> List[str]:
        return ["geometry.range", "geometry.time_extremes"]
        
    def evaluate(self, states: Dict[str, BaseState]) -> Optional[BooleanFeature]:
        range_state = states["geometry.range"]
        extremes = states["geometry.time_extremes"]
        
        # Stub logic for evaluation
        is_breakout = False
        if not range_state.in_range and extremes.pdh > 0:
            is_breakout = True
            
        return BooleanFeature(
            context=self.context,
            feature_id=self.feature_id,
            feature_type=FeatureType("geometry.range_breakout", "Range Breakout", "Geometry"),
            version=1,
            quality=1.0,
            confidence=0.8,
            source_states={
                "geometry.range": str(range_state.version),
                "geometry.time_extremes": str(extremes.version)
            },
            produced_at=datetime.now(timezone.utc),
            metadata={"description": "Price broke out of historical range."}
        )

# Register the feature
feature_registry.register_feature(
    feature_id="geometry.range_breakout",
    feature_class=RangeBreakoutFeature,
    metadata={
        "family": "Geometry",
        "consumes_states": ["geometry.range", "geometry.time_extremes"],
        "produces_feature": "Boolean",
        "version": "1.0",
        "description": "True if price has broken out of a defined range."
    }
)
