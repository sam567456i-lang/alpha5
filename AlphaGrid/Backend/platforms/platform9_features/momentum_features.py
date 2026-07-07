from typing import Dict, Optional, List
from datetime import datetime, timezone
from Backend.core.state import BaseState
from Backend.platforms.platform9_features.feature_base import FeatureType, BooleanFeature, FloatFeature
from Backend.platforms.platform9_features.feature_framework import FeaturePlugin
from Backend.platforms.platform9_features.feature_registry import feature_registry

class MomentumDivergenceFeature(FeaturePlugin):
    @property
    def feature_id(self) -> str:
        return "momentum.divergence"
        
    @property
    def required_states(self) -> List[str]:
        return ["momentum.oscillator"]
        
    def evaluate(self, states: Dict[str, BaseState]) -> Optional[BooleanFeature]:
        mom_state = states["momentum.oscillator"]
        
        return BooleanFeature(
            context=self.context,
            feature_id=self.feature_id,
            feature_value=False, # Stub
            feature_type=FeatureType("momentum.divergence", "Momentum Divergence", "Momentum"),
            version=1,
            quality=1.0,
            confidence=0.75,
            source_states={"momentum.oscillator": str(mom_state.version)},
            produced_at=datetime.now(timezone.utc),
            metadata={"description": "Price made higher high but momentum made lower high."}
        )

feature_registry.register_feature(
    feature_id="momentum.divergence",
    feature_class=MomentumDivergenceFeature,
    metadata={
        "family": "Momentum",
        "consumes_states": ["momentum.oscillator"],
        "produces_feature": "Boolean",
        "version": "1.0",
        "description": "True if divergence is detected."
    }
)
