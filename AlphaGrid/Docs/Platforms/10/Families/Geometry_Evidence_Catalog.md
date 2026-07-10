---
Authority: Level 2
Parent: Docs/Platforms/10/Families/Geometry_Specification.md
Type: Evidence Catalog
Domain: Primitives
Platform: 10
Version: 1.0.0
Status: ACTIVE
CRL: CRL-2
---

# Geometry Evidence Catalog

This catalog enumerates the objective mathematical data contracts produced by the Geometry Family. 

| Evidence DTO | Producer Engine | Downstream Consumers | Status |
|---|---|---|---|
| **DistanceEvidence** | DistanceEngine | Liquidity Objects, P11 Profiles | Designed |
| **VectorEvidence** | AngleVectorEngine | Structure Geometry, P11 Profiles | Designed |
| **IntersectionEvidence** | IntersectionEngine | Liquidity Events, Structure Events | Designed |
| **ContainmentEvidence** | IntersectionEngine | Liquidity Events, Structure Events | Designed |
| **ExtensionEvidence** | ExtensionEngine | P11 Profiles | Designed |
| **RatioEvidence** | ExtensionEngine | P11 Profiles | Designed |
| **AlignmentEvidence** | SpatialEngine | Pattern Recognition, P11 Profiles | Designed |
| **ParallelEvidence** | SpatialEngine | Trendlines, Channels | Designed |
| **PerpendicularEvidence** | SpatialEngine | Geometric Tools | Designed |
| **OverlapEvidence** | SpatialEngine | Liquidity | Designed |
| **TouchEvidence** | SpatialEngine | Liquidity Events | Designed |
| **SeparationEvidence** | SpatialEngine | Void Analysis | Designed |
| **CoincidenceEvidence** | SpatialEngine | Convergence | Designed |

## DTO Definitions
These structs will be implemented in Python as `dataclass` objects in `Backend.core.evidence_dtos.geometry`.

### DistanceEvidence
```python
@dataclass(frozen=True)
class DistanceEvidence:
    asset: str
    timeframe: str
    timestamp: int
    distance_price: float
    distance_time: int
    distance_ticks: float
    distance_atr: float
```

### VectorEvidence
```python
@dataclass(frozen=True)
class VectorEvidence:
    asset: str
    timeframe: str
    timestamp: int
    slope: float
    angle_degrees: float
    vector_dp: float
    vector_dt: int
```

### IntersectionEvidence
```python
@dataclass(frozen=True)
class IntersectionEvidence:
    asset: str
    timeframe: str
    timestamp: int
    intersection_price: float
    intersection_timestamp: int
    intersected_object_type: str # e.g. "Ray", "RangeBoundary"
```

### ContainmentEvidence
```python
@dataclass(frozen=True)
class ContainmentEvidence:
    asset: str
    timeframe: str
    timestamp: int
    is_contained: bool
    containment_percentage: float
    container_object_type: str # e.g. "Range"
```

### ProjectionEvidence
```python
@dataclass(frozen=True)
class ProjectionEvidence:
    asset: str
    timeframe: str
    timestamp: int
    projected_price: float
    projection_ratio: float
```
