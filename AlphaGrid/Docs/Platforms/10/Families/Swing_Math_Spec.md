---
Authority: Level 2
Parent: Docs/Platforms/10/Families/Swing_Specification.md
Type: Mathematical Specification
Domain: Primitives
Platform: 10
Version: 1.0.0
Status: ACTIVE
CRL: CRL-2
---

# Swing Family Mathematical Specification

This specification strictly documents the mathematical formulas, time complexities, and algorithmic properties of the Swing engines.

## 1. Pivot Detection Engine (Pluggable)
The engine strictly abstracts the algorithm using the `PivotDetectionPolicy` interface.

### 1.1 N-Bar Fractal Policy
- **Formula:** A point `P_t` is a Pivot High if `High_t > High_{t-i}` and `High_t > High_{t+i}` for `i` in `[1, N]`.
- **Complexity:** `O(N)` per bar.
- **Numeric Stability:** If multiple highs are strictly equal, the latest is favored to ensure forward progression.

### 1.2 ATR-Based Adaptive Policy
- **Formula:** Retracement > `K * ATR(N)`. A pivot is locked when price reverses from an extreme by the ATR threshold.
- **Inputs:** `VolatilityEvidence` (ATR).
- **Complexity:** `O(1)` streaming.

### 1.3 ZigZag Policy (Registered)
- **Formula:** Pending implementation. Will filter swings below a defined percentage or absolute price movement.
- **Status:** Registered Placeholder.

### 1.4 ATR Pivot Policy (Registered)
- **Formula:** Pending implementation. Will filter swings using a dynamic ATR multiplier threshold.
- **Status:** Registered Placeholder.

## 2. Persistence Engine (Lifecycle & Revision Policy)
### State Transitions
- **Candidate:** The point is a suspected pivot.
- **Developing:** The point has survived `N/2` bars.
- **Confirmed:** The point has survived `N` bars or ATR threshold.
- **Active:** Currently the most recent confirmed swing.
- **Invalidated:** Price sweeps the pivot while still in `Candidate` or `Developing` state.
- **Archived:** Surpassed by a newer active swing.

### Pivot Revision Policy
- **Immutable:** Once a pivot transitions to `Confirmed`, its `timestamp`, `price`, and `pivot_type` are strictly immutable. It may never be edited. It can only transition state to `Active` and then `Archived` as it is superseded.

## 3. Relationship Engine
### Proximity Thresholds & Equality Specification
To compute "Equal Highs", absolute equality is rarely practical due to floating-point and spread variances.
- **Formula:** `abs(High_A - High_B) <= max(Tolerance * ATR, TickSize * n)`
- **Variables:**
  - `Tolerance`: A multiplier (e.g. 0.1) against current ATR.
  - `TickSize`: The absolute minimum tick value of the asset.
  - `n`: Number of ticks allowed.
- **Relationships:**
  - `Higher High (HH)`: `High_B > High_A + max(Tolerance * ATR, TickSize * n)`
  - `Lower High (LH)`: `High_B < High_A - max(Tolerance * ATR, TickSize * n)`
  - `Equal High (EQH)`: `abs(High_B - High_A) <= max(Tolerance * ATR, TickSize * n)`
  - `Near Equal High (NEQH)`: `abs(High_B - High_A) <= 2 * max(Tolerance * ATR, TickSize * n)`

## 4. Hierarchy Engine
### Recursive Tree Mapping
- **Formula:** A swing at scale `S` contains sub-swings at scale `S-1` if their timestamps `t_start` and `t_end` fall strictly within the domain of the parent swing.
- **Tree Complexity Limits:**
  - **Maximum Depth:** 5 hierarchical levels.
  - **Maximum Children:** 100 per parent swing.
  - **Traversal Complexity:** `O(N)` breadth-first traversal guarantees bounded execution time.
  - **Serialization Format:** Flat adjacency list to guarantee `O(1)` memory lookup.

## 5. Quality Engine
### Objective Significance Metrics
- **Magnitude:** `abs(Pivot_A.price - Pivot_B.price)`
- **Duration:** `Pivot_B.timestamp - Pivot_A.timestamp`
- **Symmetry:** `min(Duration_Up, Duration_Down) / max(Duration_Up, Duration_Down)`
- **Volatility-Adjusted Significance:** `Magnitude / ATR`
