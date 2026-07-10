---
Authority: Level 2
Parent: Docs/Governance/Platform10_Family_Development_Standard.md
Domain: Primitives
Platform: 10
Family: Range
Version: 1.0.0
Status: ACTIVE
CRL: CRL-1
---

# Range Family Charter

## 1. Purpose
The Range Family extracts and manages objective bounded price geometry. It translates combinations of `SwingEvidence` (Pivots) and `PriceEvidence` into spatial zones defined by a high boundary, low boundary, midpoint, and width. 

## 2. Scope
The Range Family measures the following objective dimensions:
- **Range Boundaries:** Range High, Range Low, Midpoint.
- **Range Geometry:** Width, Duration.
- **Range State:** Compression, Expansion, Consolidation.
- **Hierarchical Ranges:** Internal Range (sub-ranges within a master range), External Range (the master range).
- **Temporal Ranges:** Opening Range, Session Range (anchored by time, independent of swings).

## 3. Explicit Non-Goals (Out of Scope)
Per Platform 10 Governance Rules 4 & 5, the Range Family **shall not**:
- Independently detect swings or pivots (must consume `SwingEvidence`).
- Detect Liquidity (no sweep analysis or liquidity pools).
- Publish Market Structure (no BOS/CHoCH).
- Embed methodology-specific labels (e.g., Accumulation, Distribution).

## 4. Upstream Dependencies
- `PriceEvidence` (OHLCV)
- `TimeEvidence` (for Opening/Session ranges)
- `StatisticsEvidence` (Distribution profiling within a range)
- `SwingEvidence` (Pivot anchoring for structural ranges)

## 5. Downstream Consumers
- **Platform 10 Families:** Geometry (range-based channels), Liquidity (range liquidity), Institutional Zones (Premium/Discount anchors), Imbalance.
- **Platform 11 Profiles:** ICT (Premium/Discount arrays, Asian Range), SMC, Wyckoff (TR definition), AMT (Value Areas).

## 6. Success Criteria
1. **Pure Consumer:** Range never runs a pivot detection algorithm.
2. **Determinism:** Range Boundaries are mathematical constraints, not subjective drawings.
3. **Internal vs External:** Robust recursive mapping of internal ranges nesting within external ranges without infinite loops.
4. **Time vs Structure:** Gracefully handles ranges defined strictly by time (e.g. 09:30-10:00) vs ranges defined by swing points.
