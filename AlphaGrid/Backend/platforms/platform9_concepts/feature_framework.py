from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Type, Set
from datetime import datetime, timezone

from Backend.core.state import ExecutionContext, BaseState
from Backend.platforms.platform9_concepts.feature_base import BaseFeature, FeatureType, BooleanFeature, FloatFeature
from Backend.platforms.platform9_concepts.feature_registry import feature_registry

class FeaturePlugin(ABC):
    """
    Base class for all Platform 9 Feature Plugins.
    Strictly consumes BaseState and produces BaseFeature.
    No indicators, no raw market data.
    """
    def __init__(self, context: ExecutionContext):
        self.context = context
        
    @property
    @abstractmethod
    def feature_id(self) -> str:
        """Unique ID of the feature."""
        pass
        
    @property
    @abstractmethod
    def required_states(self) -> List[str]:
        """List of State IDs this feature strictly requires."""
        pass
        
    @abstractmethod
    def evaluate(self, states: Dict[str, BaseState]) -> Optional[BaseFeature]:
        """
        Evaluate the states and produce a Feature.
        Returns None if conditions are not met to produce the feature.
        """
        pass
        
    def validate_inputs(self, states: Dict[str, BaseState]) -> bool:
        """
        Ensure all required states are present before evaluation.
        """
        for req in self.required_states:
            if req not in states:
                return False
        return True

class FeatureDependencyResolver:
    """
    Ensures that when features are requested, their required states are identified.
    Since Features do not depend on other Features (only States), this is simpler than Platform 8.
    """
    @staticmethod
    def resolve_required_states(feature_ids: List[str]) -> Set[str]:
        required = set()
        for fid in feature_ids:
            metadata = feature_registry.get_metadata(fid)
            required.update(metadata.get("consumes_states", []))
        return required

class FeatureValidator:
    """
    Validates that a produced Feature strictly conforms to Platform 9 purity rules.
    """
    @staticmethod
    def validate(feature: BaseFeature) -> bool:
        if not isinstance(feature, (BooleanFeature, FloatFeature)):
            return False
        if not feature.source_states:
            return False
        if not feature.context:
            return False
        return True

class FeatureCache:
    """
    In-memory cache for features during a session.
    """
    def __init__(self):
        self._cache: Dict[str, BaseFeature] = {}
        
    def set(self, feature: BaseFeature):
        self._cache[feature.feature_id] = feature
        
    def get(self, feature_id: str) -> Optional[BaseFeature]:
        return self._cache.get(feature_id)

class FeatureStore:
    """
    Persistence layer for features (stubbed for DB).
    """
    pass

class FeatureCompiler:
    """
    Orchestrates the evaluation of multiple Feature Plugins.
    """
    def __init__(self, context: ExecutionContext):
        self.context = context
        self.plugins: List[FeaturePlugin] = []
        self.cache = FeatureCache()
        self.validator = FeatureValidator()
        
    def load_plugins(self, feature_ids: List[str]):
        """Load plugins by their registered IDs."""
        for fid in feature_ids:
            plugin_class = feature_registry.get_feature(fid)
            self.plugins.append(plugin_class(self.context))
            
    def compile(self, states: Dict[str, BaseState]) -> Dict[str, BaseFeature]:
        features = {}
        for plugin in self.plugins:
            if plugin.validate_inputs(states):
                try:
                    feature = plugin.evaluate(states)
                    if feature and self.validator.validate(feature):
                        features[plugin.feature_id] = feature
                        self.cache.set(feature)
                except Exception as e:
                    pass
        return features

class FeatureMetrics:
    """Tracks performance and hit-rates of feature extraction."""
    pass

class FeatureExplainabilityMapping:
    """Maps feature extractions to textual explainability templates."""
    pass
