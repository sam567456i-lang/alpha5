---
Authority: Level 1
Parent: Docs/Governance/Constitution.md
Type: Architectural Decision Record
Title: ADR-GEOM-001 Geometry Family Redefinition
Status: ACTIVE
Date: 2026-07-09
---

# ADR-GEOM-001: Geometry Family Redefinition

## 1. Context
Initially, the Geometry Family was scoped as an object detector (e.g. channel detection). This risked overlapping responsibilities with Swing, Trend, and Range, potentially violating the Single Source of Truth rule. Furthermore, downstream logic (like Liquidity Sweeps or Structure Breaks) requires complex Euclidean intersections that didn't have a clear owner.

## 2. Decision
We redefine the Geometry Family as the universal **Mathematical Relationship Engine**.

### 2.1 Pure Consumer Rule
The Geometry Family will **never** consume raw price candles to detect shapes. It consumes abstract primitives (`SwingEvidence`, `RangeBoundaryEvidence`, `TrendEvidence`) and calculates the spatial reality between them.

### 2.2 Mathematical Orthogonality
Geometry produces raw mathematical facts (e.g., Object A intersects Object B at Timestamp C). It explicitly avoids assigning subjective methodology labels to these facts. (It produces an "Intersection", not a "Liquidity Sweep" or "BOS").

### 2.3 Strict Determinism
All spatial relationships must be computed using Euclidean or absolute formulas with bounded complexity (`O(1)` where possible) and robust handling for infinite boundaries (vertical slopes) or zero-width denominators.

## 3. Consequences
- **Positive:** Creates an incredibly powerful chokepoint. Market Structure and Liquidity Families no longer need to write complex intersection math; they simply subscribe to `IntersectionEvidence` and apply their specific semantic logic.
- **Negative:** Highly dependent on the accuracy of upstream primitive extraction.
