---
Authority: Level 2
Parent: Docs/Governance/Platform10_Family_Development_Standard.md
Domain: Primitives
Platform: 10
Family: Swing
Version: 1.0.0
Status: ACTIVE
CRL: CRL-1
---

# Swing Family Charter

## 1. Purpose
The Swing Family owns **only objective pivot extraction and swing relationships**. It converts raw market price and statistics into a recursive tree of swing points, managing their complete lifecycle from candidate to archived.

## 2. Scope
The Swing Family measures the following objective dimensions:
- **Pivot Detection (Pluggable):** Configurable pivot algorithms (N-Bar, ZigZag, ATR, etc.).
- **Pivot Lifecycle:** Candidate -> Developing -> Confirmed -> Active -> Invalidated -> Archived.
- **Classification:** Hierarchical and recursive tree classification.
- **Relationships:** HH, HL, LH, LL, Equal High, Equal Low, Near Equal High, Near Equal Low, Higher Equal, Lower Equal.
- **Quality:** Magnitude, Duration, Symmetry, Volatility-adjusted significance, Confirmation bars.

## 3. Explicit Non-Goals (Out of Scope)
Per Platform 10 Governance Rule 5 (No Semantic Inflation), the Swing Family **shall not**:
- Publish Market Structure (no BOS, CHoCH, MSS, Trend Reversals).
- Publish Liquidity (no Sweeps, Stop Hunts).
- Compute Trend (it may be consumed by Trend, but it does not compute directional persistence itself).
- Embed methodology-specific labels (e.g., Wyckoff, ICT).

## 4. Upstream Dependencies
- `PriceEvidence` (OHLCV)
- `TimeEvidence`
- `StatisticsEvidence` (Specifically Volatility for adaptive pivots, and Distribution). 
*(Note: Trend is optionally a consumer, but Swing does NOT depend on Trend.)*

## 5. Downstream Consumers
- **Platform 10 Families:** Range (boundaries), Geometry (trendlines, channels), Liquidity (EQH/EQL, swing liquidity), Market Structure (BOS/CHOCH foundation), Imbalance (anchoring).
- **Platform 11 Profiles:** ICT, SMC, Wyckoff, AMT interpretations.

## 6. Success Criteria
1. **Pluggability:** The pivot detection engine strictly abstracts the algorithm (N-bar vs ATR) through a `PivotDetectionPolicy` interface.
2. **Recursive Trees:** Swings are modeled hierarchically (Primary -> Secondary -> Minor) rather than in flat, rigid tiers.
3. **Comprehensive Datasets:** Family passes validation against flat markets, steady trends, double tops, equal highs, gap opens, volatility spikes, long consolidations, and noisy markets.
4. **Lifecycle Fidelity:** Downstream consumers cannot mistakenly bind to unconfirmed ("Candidate" or "Developing") pivots without explicit intent.
