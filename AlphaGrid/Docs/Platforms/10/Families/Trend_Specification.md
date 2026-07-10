---
Authority: Level 2
Parent: Docs/Governance/Platform10_Family_Development_Standard.md
Type: Capability Family Specification
Domain: Trend
Platform: 10
Version: 1.0.0
Status: ACTIVE
CRL: CRL-2
---

# Trend Family Specification

**Family:** Trend
**Owns:** ✓ Measurement, ✓ Quality
**Consumes:** ✓ Statistics, ✓ Price
**Publishes:** ✓ DirectionalEvidence, ✓ MomentumEvidence, ✓ SmoothnessEvidence
**Never Publishes:** ✗ Objects, ✗ Events, ✗ Methodology Terms, ✗ Swings

## 1. Scope Definition
The **Trend Family** converts raw numerical properties from Price, Time, and Statistics into structural, objective evidence representing the directional persistence of an asset over time. 

It does **not** evaluate market structure logic (BOS, CHoCH) or apply predictive methodology interpretations (e.g., Markdown/Markup).

## 2. Engine Components
The family is composed of the following orchestrated engines:

### 2.1 Direction Engine
- **Purpose:** Classifies the directional bias and emits `TrendDirectionEvidence`.
- **Inputs:** `RollingStatisticsEvidence` (SMA/EMA).
- **Outputs:** Up, Down, Neutral.

### 2.2 Strength Engine
- **Purpose:** Quantifies the magnitude of the trend using statistical inputs.
- **Inputs:** `VolatilityEvidence` (ATR, TR).
- **Outputs:** `TrendStrengthEvidence` (Raw score + Weak, Moderate, Strong). Note: Hard thresholds are stored in Rules, not the Engine itself.

### 2.3 Geometry Engine
- **Purpose:** Computes continuous measurements of the price curve.
- **Inputs:** `PriceEvidence` and `RollingStatisticsEvidence`.
- **Outputs:** `TrendSlopeEvidence`, `TrendAccelerationEvidence` (Raw values).

### 2.4 State Engine
- **Purpose:** Detects the current objective condition of the market.
- **Inputs:** `TrendDirectionEvidence`, `TrendGeometryEvidence`, `VolatilityEvidence`.
- **Outputs:** `TrendStateEvidence` (Impulse, Correction, Expansion, Compression, Consolidation, Transition).

### 2.5 Persistence Engine
- **Purpose:** Measures the duration and consistency of the trend.
- **Inputs:** `TimeEvidence`, `TrendDirectionEvidence`.
- **Outputs:** `TrendPersistenceEvidence` (Increasing, Stable, Weakening).

## 3. Certification Gates
This family cannot be marked complete until all engines pass the strict 19-step standard execution lifecycle, culminating in a `Trend_Certification.md` report.
