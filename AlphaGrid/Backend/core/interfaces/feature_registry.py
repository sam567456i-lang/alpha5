from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Any

class FeatureGroup(Enum):
    TREND = "TREND"
    MOMENTUM = "MOMENTUM"
    LIQUIDITY = "LIQUIDITY"
    STRUCTURE = "STRUCTURE"
    VOLUME = "VOLUME"
    PROFILE = "PROFILE"
    ORDER_FLOW = "ORDER_FLOW"
    CROSS_MARKET = "CROSS_MARKET"
    STATISTICS = "STATISTICS"

class NormalizationType(Enum):
    NATURAL = "NATURAL"
    Z_SCORE = "Z_SCORE"
    PERCENTILE = "PERCENTILE"
    MIN_MAX = "MIN_MAX"
    SIGMOID = "SIGMOID"
    TANH = "TANH"

@dataclass(frozen=True)
class FeatureValidationConstraints:
    allowed_range: tuple[float, float]
    expected_units: str
    null_handling: str
    required_capabilities: List[str]

@dataclass(frozen=True)
class FeatureMetadata:
    """The authoritative API contract for a published feature."""
    feature_id: str
    version: str
    group: FeatureGroup
    data_type: str
    normalization: NormalizationType
    update_frequency: str
    dependencies: List[str]
    validation_constraints: FeatureValidationConstraints
    consumer_platforms: List[str]

class FeatureRegistry:
    """Central registry validating all features before publication."""
    def __init__(self):
        self._catalog: Dict[str, FeatureMetadata] = {}

    def register(self, metadata: FeatureMetadata):
        key = f"{metadata.feature_id}.{metadata.version}"
        self._catalog[key] = metadata

    def get_feature(self, feature_id: str, version: str) -> FeatureMetadata:
        key = f"{feature_id}.{version}"
        if key not in self._catalog:
            raise KeyError(f"Unregistered feature: {key}")
        return self._catalog[key]
