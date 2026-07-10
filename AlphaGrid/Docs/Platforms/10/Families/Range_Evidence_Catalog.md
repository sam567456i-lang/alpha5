---
Authority: Level 2
Parent: Docs/Platforms/10/Families/Range_Specification.md
Type: Evidence Catalog
Domain: Primitives
Platform: 10
Version: 1.0.0
Status: ACTIVE
CRL: CRL-2
---

# Range Evidence Catalog

This catalog enumerates the objective data contracts produced by the Range Family. 

| Evidence DTO | Producer Engine | Downstream Consumers | Status |
|---|---|---|---|
| **RangeBoundaryEvidence** | BoundaryEngine | GeometryEngine, HierarchyEngine, Liquidity, Structure | Designed |
| **TemporalRangeEvidence** | TemporalEngine | GeometryEngine, P11 Profiles | Designed |
| **RangeGeometryEvidence** | GeometryEngine | StateEngine | Designed |
| **RangeStateEvidence** | StateEngine | Imbalance, P11 Profiles | Designed |
| **RangeHierarchyEvidence** | HierarchyEngine | P11 Profiles | Designed |

## DTO Definitions
These structs will be implemented in Python as `dataclass` objects in `Backend.core.evidence_dtos.range`.

### RangeBoundaryEvidence
```python
@dataclass(frozen=True)
class RangeBoundaryEvidence:
    asset: str
    timeframe: str
    timestamp: int
    range_high: float
    range_low: float
    midpoint: float
    origin_timestamp: int
```

### TemporalRangeEvidence
```python
@dataclass(frozen=True)
class TemporalRangeEvidence:
    asset: str
    timeframe: str
    timestamp: int
    range_high: float
    range_low: float
    midpoint: float
    start_time: int
    end_time: int
```

### RangeGeometryEvidence
```python
@dataclass(frozen=True)
class RangeGeometryEvidence:
    asset: str
    timeframe: str
    timestamp: int
    width_ticks: float
    width_percentage: float
    duration_bars: int
```

### RangeStateEvidence
```python
@dataclass(frozen=True)
class RangeStateEvidence:
    asset: str
    timeframe: str
    timestamp: int
    state: str # "Compression" | "Expansion" | "Consolidation"
```

### RangeHierarchyEvidence
```python
@dataclass(frozen=True)
class RangeHierarchyEvidence:
    asset: str
    timeframe: str
    timestamp: int
    is_internal: bool
    parent_range_timestamp: Optional[int]
```
