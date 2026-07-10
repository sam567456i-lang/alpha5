---
Authority: Level 2
Parent: Docs/Governance/Platform10_Family_Development_Standard.md
Type: Capability Family Specification
Domain: Primitives
Platform: 10
Version: 1.0.0
Status: ACTIVE
CRL: CRL-2
---

# Range Family Specification

**Family:** Range
**Owns:** ✓ Object
**Consumes:** ✓ Swing, ✓ Time, ✓ Price, ✓ Statistics
**Publishes:** ✓ RangeBoundaryEvidence, ✓ TemporalRangeEvidence, ✓ RangeGeometryEvidence, ✓ RangeStateEvidence, ✓ RangeHierarchyEvidence
**Never Publishes:** ✗ Events, ✗ Methodology Terms, ✗ Liquidity Pools, ✗ BOS

## 1. Domain Definition
The **Range Family** calculates and manages objective, bounded price geometry. It does not perform pivot extraction; instead, it consumes `SwingEvidence` and `TimeEvidence` to define explicit spatial constraints (Ranges). 

Per Governance Rules 4 & 5, it explicitly **does not** compute BOS (Break of Structure) or Liquidity Sweeps, and it cannot recalculate pivots.

## 2. Engine Components
The family is composed of the following five orchestrated engines:

### 2.1 Boundary Engine
- **Purpose:** Determines the absolute Range High, Range Low, and Midpoint based on structural pivots or dynamic price containment.
- **Inputs:** `SwingEvidence` (Pivots, HH/LL), `PriceEvidence`.
- **Outputs:** `RangeBoundaryEvidence`.

### 2.2 Temporal Engine
- **Purpose:** Generates non-structural ranges anchored strictly by time constraints (e.g., Opening Range, Session Range).
- **Inputs:** `TimeEvidence`, `PriceEvidence`.
- **Outputs:** `TemporalRangeEvidence`.

### 2.3 Geometry Engine
- **Purpose:** Computes the scalar properties of a defined range boundary.
- **Inputs:** `RangeBoundaryEvidence`, `TemporalRangeEvidence`.
- **Outputs:** `RangeGeometryEvidence` (Width in absolute ticks/percentage, Duration in bars/seconds).

### 2.4 State Engine
- **Purpose:** Classifies the dynamic behavior of price relative to the range and previous ranges.
- **Inputs:** `RangeGeometryEvidence`, `StatisticsEvidence` (Volatility).
- **Outputs:** `RangeStateEvidence` (Consolidation, Compression, Expansion).

### 2.5 Hierarchy Engine
- **Purpose:** Maps the nesting relationships between ranges to distinguish master containers from local containers.
- **Inputs:** `RangeBoundaryEvidence`.
- **Outputs:** `RangeHierarchyEvidence` (External Range, Internal Range).

## 3. Certification Gates
This family cannot be marked complete until all engines pass the strict 19-step standard execution lifecycle, culminating in a `Range_Certification.md` report.
