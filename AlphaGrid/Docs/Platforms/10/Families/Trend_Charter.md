---
Authority: Level 2
Parent: Docs/Governance/Platform10_Family_Development_Standard.md
Domain: Foundation
Platform: 10
Family: Trend
Version: 1.0.0
Status: ACTIVE
CRL: CRL-1
---

# Trend Family Charter

## 1. Purpose
Trend measures objective directional behavior only. It does not detect market structure, identify methodology concepts, or own swing analysis. It publishes reusable trend evidence that downstream families and Platform 11 profiles may consume.

Trend is an objective description of directional persistence, separated into distinct, measurable dimensions. 

## 2. Scope
The Trend Family measures the following objective dimensions:
- **Direction:** Up, Down, Neutral
- **Strength:** Weak, Moderate, Strong (alongside raw strength measurements)
- **Persistence:** Increasing, Stable, Weakening
- **Geometry:** Slope, Curvature, Acceleration
- **Structure State:** Impulse, Correction, Expansion, Compression, Consolidation, Transition

## 3. Explicit Non-Goals (Out of Scope)
The Trend Family **shall not**:
- Expose indicator implementations as semantic concepts (e.g., no `ADXEvidence`, only `TrendStrengthEvidence`).
- Embed methodology-specific labels (e.g., no ICT Markup, no Wyckoff Accumulation).
- Embed hard thresholds inside engines (e.g., `if ADX > 25`). Engines emit measurements; configurable rules classify them.
- Own swing detection. Trend does not compute swings or Market Structure (BOS, CHoCH).

## 4. Upstream Dependencies
- `PriceEvidence` (OHLCV)
- `TimeEvidence`
- `Statistics` (`VolatilityEvidence`, `RollingStatisticsEvidence`, `DistributionEvidence`)

## 5. Downstream Consumers
- **Platform 10 Families:** Swing, Market Structure, Liquidity, Institutional Zones.
- **Platform 11 Profiles:** All trend-following and mean-reversion profiles.
- **Platform 12 Decision Engine.**

## 6. Success Criteria
1. Strict separation of raw measurements (e.g., `acceleration=0.19`) from discrete classifications (e.g., `strong`).
2. Comprehensive Family Acceptance Datasets covering constant prices, linear increase, accelerating trends, oscillating ranges, and reversals.
3. 100% replay determinism and no methodology leakage.
