---
Authority: Level 2
Parent: Docs/Platforms/10/Families/Geometry_Specification.md
Type: Mathematical Specification
Domain: Primitives
Platform: 10
Version: 1.0.0
Status: ACTIVE
CRL: CRL-2
---

# Geometry Family Mathematical Specification

This specification strictly documents the mathematical formulas, time complexities, and numeric bounds of the Geometry engines.

## 1. Distance Engine
### 1.1 Spatial Measurements
- **Price Distance (`dp`):** `abs(Price_A - Price_B)`
- **Time Distance (`dt`):** `abs(Timestamp_A - Timestamp_B)`
- **Tick Normalized Distance:** `dp / TickSize`
- **ATR Normalized Distance:** `dp / ATR`
- **Complexity:** `O(1)`.

## 2. Angle & Vector Engine
### 2.1 Slope & Vectors
- **Slope (`m`):** `(Price_B - Price_A) / (Timestamp_B - Timestamp_A)`
  - *Numerical Stability:* If `Timestamp_B == Timestamp_A`, slope is strictly evaluated as `Infinity` or handled via exception fallback, never allowing `ZeroDivisionError`.
- **Vector:** `[dp, dt]`
- **Complexity:** `O(1)`.

## 3. Intersection & Containment Engine
### 3.1 Containment bounds
- **Full Containment:** Object A is contained by Range B iff:
  - `Price_A <= B.RangeHigh` AND `Price_A >= B.RangeLow`
- **Percentage Containment:** `(Price_A - B.RangeLow) / (B.RangeHigh - B.RangeLow)`
  - *Numerical Stability:* If `B.RangeHigh == B.RangeLow`, Percentage Containment is evaluated to `1.0` if `Price_A == B.RangeHigh` else `0.0`.
- **Complexity:** `O(1)`.

### 3.2 Dynamic Intersection
- **Ray Intersection:** Given a Ray defined by `y(t) = m * (t - t_0) + y_0` and a Price boundary `Price_Target`.
- **Time of Intersection (`t_int`):** `t_int = (Price_Target - y_0) / m + t_0`
  - *Numerical Stability:* If `m == 0`, Ray is perfectly horizontal and will never intersect unless `y_0 == Price_Target`. Evaluated as `Infinity`.

## 4. Extension & Ratio Engine
### 4.1 Generic Extensions
- **Extension Formula:** `y_ext = y_base + Extension_Ratio * (y_high - y_low)`
- **Symmetry Ratio:** `abs(y_current - y_start) / max(abs(y_end - y_start), TickSize)`
- **Complexity:** `O(1)`.

## 5. Numerical Robustness Guarantees
Geometry operations must safely handle the following edge cases without exceptions:
- **Extremely large prices:** No overflow on exponentiation.
- **Extremely small tick sizes:** Floating point limits.
- **Floating-point tolerance:** Equality tests must use `abs(A-B) <= epsilon`.
- **Identical timestamps:** Evaluated as vertical infinite slopes or zero-distance time jumps.
- **Identical prices:** Evaluated as zero-height bounds.
