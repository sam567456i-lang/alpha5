from typing import Dict, Optional, List
from datetime import datetime, timezone
from Backend.core.state import BaseState
from Backend.platforms.platform9_concepts.feature_base import FeatureType, BooleanFeature, FloatFeature
from Backend.platforms.platform9_concepts.feature_framework import FeaturePlugin
from Backend.platforms.platform9_concepts.feature_registry import feature_registry

class PinbarRejectionFeature(FeaturePlugin):
    @property
    def feature_id(self) -> str:
        return "price_action.pinbar_rejection"
        
    @property
    def required_states(self) -> List[str]:
        return ["price_action.candlestick"]
        
    def evaluate(self, states: Dict[str, BaseState]) -> Optional[BooleanFeature]:
        pa_state = states["price_action.candlestick"]
        
        return BooleanFeature(
            context=self.context,
            feature_id=self.feature_id,
            feature_value=True, # Stub
            feature_type=FeatureType("price_action.pinbar_rejection", "Pinbar Rejection", "Price Action"),
            version=1,
            quality=1.0,
            confidence=0.9,
            source_states={"price_action.candlestick": str(pa_state.version)},
            produced_at=datetime.now(timezone.utc),
            metadata={"description": "Pinbar candlestick detected."}
        )

feature_registry.register_feature(
    feature_id="price_action.pinbar_rejection",
    feature_class=PinbarRejectionFeature,
    metadata={
        "family": "Price Action",
        "consumes_states": ["price_action.candlestick"],
        "produces_feature": "Boolean",
        "version": "1.0",
        "description": "True if pinbar rejection is detected."
    }
)
