from typing import List, Optional
from datetime import datetime
from Backend.core.interfaces.feature_registry import FeatureRegistry, NormalizationType
from Backend.core.evidence_dtos.features import RawFeature, FeatureVector, FeatureQuality
from Backend.core.evidence_dtos.base import PlatformIdentity, LineageRecord

class FeatureGenerationEngine:
    """Extracts raw signals from Platform 10 objects into Natural Domain features."""
    def generate_trend_strength(self, trend_object) -> RawFeature:
        # Simulated logic
        return RawFeature(
            identity=PlatformIdentity(owner_family="FeatureEngineering"),
            lineage=LineageRecord("Platform10", "FeatureEngineering", "TrendStrengthGen", [], [], "FeatureGenerationEngine", [], "1.0", "1.0", "", datetime.now()),
            feature_id="trend.strength",
            feature_version="v1",
            raw_value=5.5, # Natural domain (e.g., ADX value)
            quality=FeatureQuality(1.0, 1.0, 0.9, False, False, 1.5)
        )

class NormalizationEngine:
    """Transforms Natural Domain features into ML Vectors based on Registry definitions."""
    def __init__(self, registry: FeatureRegistry):
        self.registry = registry

    def normalize(self, raw: RawFeature) -> FeatureVector:
        # Validate against registry
        meta = self.registry.get_feature(raw.feature_id, raw.feature_version)
        
        # Apply transformation
        normalized_val = raw.raw_value
        if meta.normalization == NormalizationType.MIN_MAX:
            min_v, max_v = meta.validation_constraints.allowed_range
            normalized_val = (raw.raw_value - min_v) / (max_v - min_v)
            # Clamp bounds
            normalized_val = max(0.0, min(1.0, normalized_val))
            
        return FeatureVector(
            identity=PlatformIdentity(owner_family="FeatureEngineering"),
            lineage=LineageRecord("Platform10", "FeatureEngineering", "Normalization", [], [], "NormalizationEngine", [], "1.0", "1.0", "", datetime.now()),
            feature_id=raw.feature_id,
            feature_version=raw.feature_version,
            normalized_value=normalized_val,
            quality=raw.quality
        )
