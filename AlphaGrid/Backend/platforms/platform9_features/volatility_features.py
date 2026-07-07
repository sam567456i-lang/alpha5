from typing import Dict, Optional, List
from datetime import datetime, timezone
from Backend.core.state import BaseState
from Backend.platforms.platform9_features.feature_base import FeatureType, BooleanFeature, FloatFeature
from Backend.platforms.platform9_features.feature_framework import FeaturePlugin
from Backend.platforms.platform9_features.feature_registry import feature_registry

class VolatilityContractionFeature(FeaturePlugin):
    @property
    def feature_id(self) -> str:
        return "volatility.contraction"
        
    @property
    def required_states(self) -> List[str]:
        return ["volatility.bands"]
        
    def evaluate(self, states: Dict[str, BaseState]) -> Optional[BooleanFeature]:
        vol_state = states["volatility.bands"]
        
        return BooleanFeature(
            context=self.context,
            feature_id=self.feature_id,
            feature_value=True, # Stub
            feature_type=FeatureType("volatility.contraction", "Volatility Contraction", "Volatility"),
            version=1,
            quality=1.0,
            confidence=0.85,
            source_states={"volatility.bands": str(vol_state.version)},
            produced_at=datetime.now(timezone.utc),
            metadata={"description": "Volatility is contracting (squeeze)."}
        )

feature_registry.register_feature(
    feature_id="volatility.contraction",
    feature_class=VolatilityContractionFeature,
    metadata={
        "family": "Volatility",
        "consumes_states": ["volatility.bands"],
        "produces_feature": "Boolean",
        "version": "1.0",
        "description": "True if volatility contraction is detected."
    }
)
