from typing import Dict, Optional, List
from datetime import datetime, timezone
from Backend.core.state import BaseState
from Backend.platforms.platform9_features.feature_base import FeatureType, BooleanFeature, FloatFeature
from Backend.platforms.platform9_features.feature_framework import FeaturePlugin
from Backend.platforms.platform9_features.feature_registry import feature_registry

class LiquiditySweepFeature(FeaturePlugin):
    @property
    def feature_id(self) -> str:
        return "liquidity.sweep"
        
    @property
    def required_states(self) -> List[str]:
        return ["liquidity.pool"]
        
    def evaluate(self, states: Dict[str, BaseState]) -> Optional[BooleanFeature]:
        liq_state = states["liquidity.pool"]
        
        return BooleanFeature(
            context=self.context,
            feature_id=self.feature_id,
            feature_value=True, # Stub
            feature_type=FeatureType("liquidity.sweep", "Liquidity Sweep", "Liquidity"),
            version=1,
            quality=1.0,
            confidence=0.85,
            source_states={"liquidity.pool": str(liq_state.version)},
            produced_at=datetime.now(timezone.utc),
            metadata={"description": "Liquidity pool was swept."}
        )

feature_registry.register_feature(
    feature_id="liquidity.sweep",
    feature_class=LiquiditySweepFeature,
    metadata={
        "family": "Liquidity",
        "consumes_states": ["liquidity.pool"],
        "produces_feature": "Boolean",
        "version": "1.0",
        "description": "True if a liquidity sweep occurred."
    }
)
