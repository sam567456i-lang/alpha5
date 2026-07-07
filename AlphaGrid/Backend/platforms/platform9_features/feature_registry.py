from typing import Dict, List, Type, Any, Optional
from datetime import datetime

from Backend.platforms.platform9_features.feature_base import FeatureType, BaseFeature
from Backend.foundation.base_registry import BaseRegistry

class FeatureRegistry(BaseRegistry):
    """
    Authoritative registry for all Platform 9 Feature Plugins.
    Enforces strict registration of what each feature consumes and produces.
    """
    def __init__(self):
        super().__init__(registry_name="FeatureRegistry")
        self._features: Dict[str, Type] = {}
        self._feature_metadata: Dict[str, Dict[str, Any]] = {}
        import logging
        self._logger = logging.getLogger(__name__)
        
    def register_feature(self, feature_id: str, feature_class: Type, metadata: Dict[str, Any]) -> None:
        """
        Register a feature plugin with its metadata.
        """
        if feature_id in self._features:
            raise ValueError(f"Feature {feature_id} already registered.")
            
        # Enforce metadata requirements
        required_keys = ["family", "consumes_states", "produces_feature", "version", "description"]
        for key in required_keys:
            if key not in metadata:
                raise ValueError(f"Feature {feature_id} missing required metadata: {key}")
                
        self._features[feature_id] = feature_class
        self._feature_metadata[feature_id] = metadata
        self._logger.info(f"Registered Feature: {feature_id} v{metadata['version']}")
        
    def get_feature(self, feature_id: str) -> Type:
        if feature_id not in self._features:
            raise KeyError(f"Feature {feature_id} not found in registry.")
        return self._features[feature_id]
        
    def get_metadata(self, feature_id: str) -> Dict[str, Any]:
        if feature_id not in self._feature_metadata:
            raise KeyError(f"Feature {feature_id} not found in registry.")
        return self._feature_metadata[feature_id]
        
    def list_features(self) -> List[str]:
        return list(self._features.keys())
        
    def get_features_by_family(self, family: str) -> List[str]:
        return [fid for fid, meta in self._feature_metadata.items() if meta["family"] == family]

# Global Instance
feature_registry = FeatureRegistry()
