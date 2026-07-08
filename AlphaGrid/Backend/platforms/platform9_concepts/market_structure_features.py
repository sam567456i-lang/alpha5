from typing import Dict, Optional, List
from datetime import datetime, timezone
from Backend.core.state import BaseState
from Backend.platforms.platform9_concepts.feature_base import FeatureType, BooleanFeature, FloatFeature
from Backend.platforms.platform9_concepts.feature_framework import FeaturePlugin
from Backend.platforms.platform9_concepts.feature_registry import feature_registry

class BreakOfStructureFeature(FeaturePlugin):
    @property
    def feature_id(self) -> str:
        return "market_structure.bos"
        
    @property
    def required_states(self) -> List[str]:
        return ["market_structure.trend"]
        
    def evaluate(self, states: Dict[str, BaseState]) -> Optional[BooleanFeature]:
        ms_state = states["market_structure.trend"]
        
        return BooleanFeature(
            context=self.context,
            feature_id=self.feature_id,
            feature_value=False, # Stub
            feature_type=FeatureType("market_structure.bos", "Break of Structure", "Market Structure"),
            version=1,
            quality=1.0,
            confidence=0.95,
            source_states={"market_structure.trend": str(ms_state.version)},
            produced_at=datetime.now(timezone.utc),
            metadata={"description": "Break of market structure."}
        )

feature_registry.register_feature(
    feature_id="market_structure.bos",
    feature_class=BreakOfStructureFeature,
    metadata={
        "family": "Market Structure",
        "consumes_states": ["market_structure.trend"],
        "produces_feature": "Boolean",
        "version": "1.0",
        "description": "True if a break of structure happened."
    }
)
