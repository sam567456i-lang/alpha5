---
Authority: Level 2
Parent: Docs/Platforms/10/Families/Statistics_Specification.md
Type: Evidence Catalog
Domain: Statistics
Platform: 10
Version: 1.0.0
Status: ACTIVE
CRL: CRL-2
---

# Statistics Evidence Catalog

This catalog enumerates the objective data contracts produced by the Statistics Family. 

| Evidence DTO | Producer Engine | Downstream Consumers | Status |
|---|---|---|---|
| **DistributionEvidence** | DistributionEngine | Trend, Regime, Volatility | Designed |
| **RollingStatisticsEvidence** | RollingEngine | Trend, Liquidity, Structure | Designed |
| **VolatilityEvidence** | VolatilityEngine | Trend, Structure, Liquidity | Designed |
| **NormalizationEvidence** | NormalizationEngine | Decision Engine (P12) | Designed |
| **ConfidenceEvidence** | ConfidenceEngine | P12, Replay Validations | Designed |
| **DriftEvidence** | DriftEngine | P14 Learning Platform | Designed |
| **QualityEvidence** | QualityEngine | All Platforms (Sanity checking) | Designed |

## DTO Definitions
These structs will be strictly enforced in Python as `dataclass` implementations in `Backend.core.dtos.evidence`.

### VolatilityEvidence
```python
@dataclass(frozen=True)
class VolatilityEvidence:
    asset: str
    timeframe: str
    timestamp: datetime
    atr: float
    true_range: float
    historical_volatility: float
    parkinson_volatility: float
    garman_klass_volatility: float
    volatility_regime: str # "Expanding" | "Contracting" | "Stable"
```

### DistributionEvidence
```python
@dataclass(frozen=True)
class DistributionEvidence:
    asset: str
    timeframe: str
    timestamp: datetime
    mean: float
    variance: float
    skewness: float
    kurtosis: float
    entropy: float
```
