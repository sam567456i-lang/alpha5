---
Authority: Level 2
Parent: Docs/Platforms/10/Families/Swing_Specification.md
Type: Evidence Catalog
Domain: Primitives
Platform: 10
Version: 1.0.0
Status: ACTIVE
CRL: CRL-2
---

# Swing Evidence Catalog

This catalog enumerates the objective data contracts produced by the Swing Family. 

| Evidence DTO | Producer Engine | Downstream Consumers | Status |
|---|---|---|---|
| **PivotEvidence** | PivotEngine | PersistenceEngine | Designed |
| **PivotLifecycleEvidence** | PersistenceEngine | ClassificationEngine, RelationshipEngine | Designed |
| **SwingClassificationEvidence** | ClassificationEngine | HierarchyEngine | Designed |
| **SwingRelationshipEvidence** | RelationshipEngine | HierarchyEngine, Structure, Liquidity | Designed |
| **SwingHierarchyEvidence** | HierarchyEngine | Structure, P11 Profiles | Designed |
| **SwingQualityEvidence** | QualityEngine | P11 Profiles, P12 Decision | Designed |

## DTO Definitions
These structs will be implemented in Python as `dataclass` objects in `Backend.core.evidence_dtos.swing`.

### PivotLifecycleEvidence
```python
@dataclass(frozen=True)
class PivotLifecycleEvidence:
    asset: str
    timeframe: str
    timestamp: int
    pivot_type: str # "High" | "Low"
    price: float
    state: str # "Candidate" | "Developing" | "Confirmed" | "Active" | "Invalidated" | "Archived"
```

### SwingRelationshipEvidence
```python
@dataclass(frozen=True)
class SwingRelationshipEvidence:
    asset: str
    timeframe: str
    timestamp: int
    relationship: str # "HH" | "HL" | "LH" | "LL" | "EQH" | "EQL" | "NEQH" | "NEQL" | "HEQ" | "LEQ"
    origin_pivot_timestamp: int
    current_pivot_timestamp: int
```

### SwingHierarchyEvidence
```python
@dataclass(frozen=True)
class SwingHierarchyEvidence:
    asset: str
    timeframe: str
    timestamp: int
    tree_depth: int
    parent_swing_timestamp: Optional[int]
    child_swings: List[int] # Timestamps of immediate children
```

### SwingQualityEvidence
```python
@dataclass(frozen=True)
class SwingQualityEvidence:
    asset: str
    timeframe: str
    timestamp: int
    magnitude: float
    duration: int
    symmetry_ratio: float
    volatility_adjusted_significance: float
    confirmation_bars: int
    volume_support: float
```
