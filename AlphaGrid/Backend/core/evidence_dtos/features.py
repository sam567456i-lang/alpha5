from dataclasses import dataclass, field
from Backend.core.evidence_dtos.base import BasePlatformObject, PlatformIdentity, LineageRecord

@dataclass(frozen=True)
class FeatureQuality:
    freshness: float
    completeness: float
    confidence: float
    missing_inputs: bool
    degraded_mode: bool
    calculation_latency_ms: float

@dataclass
class RawFeature(BasePlatformObject):
    """The natural domain output before normalization."""
    feature_id: str = ""
    feature_version: str = "v1"
    raw_value: float = 0.0
    quality: FeatureQuality = None

@dataclass
class FeatureVector(BasePlatformObject):
    """The final ML-ready normalized output published to downstream platforms."""
    feature_id: str = ""
    feature_version: str = "v1"
    normalized_value: float = 0.0
    quality: FeatureQuality = None
