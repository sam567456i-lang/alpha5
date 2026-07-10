---
Authority: Level 2
Parent: Docs/Platforms/10/Families/Trend_Specification.md
Type: Evidence Catalog
Domain: Trend
Platform: 10
Version: 1.0.0
Status: ACTIVE
CRL: CRL-2
---

# Trend Evidence Catalog

This catalog enumerates the objective data contracts produced by the Trend Family. 

| Evidence DTO | Producer Engine | Downstream Consumers | Status |
|---|---|---|---|
| **TrendDirectionEvidence** | DirectionEngine | StateEngine, Swing, Struct | Designed |
| **TrendStrengthEvidence** | StrengthEngine | StateEngine, Liquidity | Designed |
| **TrendSlopeEvidence** | GeometryEngine | StateEngine, P11 Profiles | Designed |
| **TrendAccelerationEvidence** | GeometryEngine | StateEngine, P11 Profiles | Designed |
| **TrendStateEvidence** | StateEngine | Swing, P11 Profiles | Designed |
| **TrendPersistenceEvidence** | PersistenceEngine | P11 Profiles | Designed |
| **TrendHierarchyEvidence** | GeometryEngine (MTF) | P12 Decision Engine | Designed |
| **TrendConfidenceEvidence** | StrengthEngine | P12 Decision Engine | Designed |
| **TrendConsistencyEvidence** | StateEngine | Swing | Designed |
| **TrendQualityEvidence** | DirectionEngine | Replay Services | Designed |

## DTO Definitions
These structs will be implemented in Python as `dataclass` objects in `Backend.core.evidence_dtos.trend`.

### TrendStateEvidence
```python
@dataclass(frozen=True)
class TrendStateEvidence:
    asset: str
    timeframe: str
    timestamp: int
    state: str # "Impulse" | "Correction" | "Expansion" | "Compression" | "Consolidation" | "Transition"
```

### TrendDirectionEvidence
```python
@dataclass(frozen=True)
class TrendDirectionEvidence:
    asset: str
    timeframe: str
    timestamp: int
    direction: str # "Up" | "Down" | "Neutral"
    raw_slope: float
```
