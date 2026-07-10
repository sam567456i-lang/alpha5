---
Authority: Level 2
Parent: Docs/Platforms/10/Families/Range_Specification.md
Type: Mathematical Specification
Domain: Primitives
Platform: 10
Version: 1.0.0
Status: ACTIVE
CRL: CRL-2
---

# Range Family Mathematical Specification

This specification strictly documents the mathematical formulas, time complexities, and algorithmic properties of the Range engines.

## 1. Boundary Engine
### 1.1 Structural Range Boundaries
- **Logic:** Consumes `SwingRelationshipEvidence` or raw `PivotLifecycleEvidence` to identify bounded price action. A common structural range is bounded by an initial Impulse Swing (High to Low, or Low to High).
- **Formula:** 
  - `RangeHigh = max(Pivot_A.price, Pivot_B.price)`
  - `RangeLow = min(Pivot_A.price, Pivot_B.price)`
  - `Midpoint = (RangeHigh + RangeLow) / 2.0`
- **Complexity:** `O(1)` upon swing confirmation.

## 2. Temporal Engine
### 2.1 Time-Bound Ranges
- **Logic:** Defines boundaries based strictly on a time window `[t_start, t_end]`.
- **Formula:**
  - `RangeHigh = max(High_t) for t in [t_start, t_end]`
  - `RangeLow = min(Low_t) for t in [t_start, t_end]`
  - `Midpoint = (RangeHigh + RangeLow) / 2.0`
- **Complexity:** `O(N)` where N is bars in the time window (can be optimized to `O(1)` per bar stream).

## 3. Geometry Engine
### 3.1 Absolute Metrics
- **Formula:** 
  - `Width_Ticks = (RangeHigh - RangeLow) / TickSize`
  - `Width_Percentage = (RangeHigh - RangeLow) / RangeLow`
  - `Duration_Bars = timestamp_end - timestamp_start`
- **Complexity:** `O(1)`.
- **Numeric Stability:** If `RangeHigh == RangeLow` (Zero-width range), `Width_Percentage = 0.0`. `Duration_Bars` allows for infinite (open-ended) durations until a range is invalidated.

## 4. State Engine
### 4.1 Volatility-Adjusted State
- **Logic:** Compares the geometry of the current range `R_n` to the preceding range `R_{n-1}` and current statistical volatility.
- **Formula:**
  - `Compression`: `R_n.Width < R_{n-1}.Width` AND `ATR_n < ATR_{n-1}`
  - `Expansion`: `R_n.Width > R_{n-1}.Width` AND `ATR_n > ATR_{n-1}`
  - `Consolidation`: Price remains strictly within `[RangeLow, RangeHigh]` for `Duration > K * ATR`.

## 5. Hierarchy Engine
### 5.1 Internal vs External
- **Formula:** A Range `R_internal` is strictly an Internal Range of `R_external` iff:
  - `R_internal.RangeHigh <= R_external.RangeHigh`
  - `R_internal.RangeLow >= R_external.RangeLow`
  - `R_internal.t_start >= R_external.t_start`
- **Complexity:** `O(log M)` tree insertion per sub-range.
