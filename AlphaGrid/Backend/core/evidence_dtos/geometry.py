from dataclasses import dataclass

@dataclass(frozen=True)
class DistanceEvidence:
    asset: str
    timeframe: str
    timestamp: int
    distance_price: float
    distance_time: int
    distance_ticks: float
    distance_atr: float

@dataclass(frozen=True)
class VectorEvidence:
    asset: str
    timeframe: str
    timestamp: int
    slope: float
    angle_degrees: float
    vector_dp: float
    vector_dt: int

@dataclass(frozen=True)
class IntersectionEvidence:
    asset: str
    timeframe: str
    timestamp: int
    intersection_price: float
    intersection_timestamp: int
    intersected_object_type: str

@dataclass(frozen=True)
class ContainmentEvidence:
    asset: str
    timeframe: str
    timestamp: int
    is_contained: bool
    containment_percentage: float
    container_object_type: str

@dataclass(frozen=True)
class ProjectionEvidence:
    asset: str
    timeframe: str
    timestamp: int
    projected_price: float
    projection_ratio: float
