---
Authority: Level 2
Parent: Docs/Governance/Platform10_Family_Development_Standard.md
Domain: Primitives
Platform: 10
Family: Geometry
Version: 1.0.0
Status: ACTIVE
CRL: CRL-1
---

# Geometry Family Charter

## 1. Purpose
The Geometry Family calculates mathematical relationships between existing objective objects (Pivots, Ranges, Trend states). It translates independent objects into relational spatial data (e.g. Distance, Angle, Intersection, Containment).

## 2. Scope
The Geometry Family measures the following objective mathematical relationships between existing entities:
- **Spatial Measurement:** Distance(A,B), Slope(A,B), Angle(A,B), Curvature.
- **Relational Interaction:** Intersection(A,B), Overlap(A,B), Containment(A,B), Parallel(LineA, LineB), Touch(A,B), Coincidence(A,B), Alignment(A,B,C).
- **Proportionality:** Extension(A,B), Ratio(A,B).

Geometry strictly owns *relationships*, not entities.

## 3. Explicit Non-Goals (Out of Scope)
Per Platform 10 Governance Rules, the Geometry Family **shall not**:
- Create or publish Objects (e.g. Trendline, Triangle, Channel, Wedge, Rectangle). Those belong to higher families.
- Detect Liquidity Events (e.g. it computes intersection, but does not label it a "Sweep").
- Embed methodology-specific rules or labels (e.g., no hardcoded Fibonacci logic; rules plugins handle ratios).

## 4. Upstream Dependencies
- `SwingEvidence` (Pivots)
- `RangeBoundaryEvidence` (Ranges)
- `TrendEvidence` (Directional vectors)
- `StatisticsEvidence` (Volatility normalizers)
- `TimeEvidence`

## 5. Downstream Consumers
- **Platform 10 Families:** Liquidity Objects (using geometry for precision pools), Structure Geometry (using geometry for complex tree alignments).
- **Platform 11 Profiles:** All methodology engines rely heavily on mathematical intersections to define setups.

## 6. Success Criteria
1. **Mathematical Purity:** Every relationship must be expressed as a strict mathematical formula (Euclidean, Absolute, or Percentage).
2. **Pure Consumer:** Geometry never touches raw `PriceEvidence` for detection. It only operates on upstream abstract objects.
3. **Numeric Stability:** Handles infinite slopes, zero distances, and overlapping timestamps without exception crashing.
