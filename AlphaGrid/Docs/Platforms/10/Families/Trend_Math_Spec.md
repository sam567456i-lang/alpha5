---
Authority: Level 2
Parent: Docs/Platforms/10/Families/Trend_Specification.md
Type: Mathematical Specification
Domain: Trend
Platform: 10
Version: 1.0.0
Status: ACTIVE
CRL: CRL-2
---

# Trend Family Mathematical Specification

This specification strictly documents the mathematical formulas, time complexities, and algorithmic properties of the Trend engines. All trend measurements consume objective statistics (Volatility, Rolling Averages) to derive geometry and state.

## 1. Geometry Engine
### Slope (First Derivative)
- **Formula:** `Slope = (Value_t - Value_{t-n}) / n` or using Linear Regression slope (β1) over window `n`.
- **Inputs:** `RollingStatisticsEvidence.rolling_mean`
- **Complexity:** `O(1)` streaming (using running covariance for LinReg).
- **Numeric Stability:** Handle flat lines (`Slope = 0`) safely.

### Acceleration (Second Derivative)
- **Formula:** `Accel_t = Slope_t - Slope_{t-1}`
- **Inputs:** `TrendSlopeEvidence`
- **Complexity:** `O(1)` streaming.

## 2. Direction Engine
### Direction Classification
- **Formula:** `Direction = UP if Slope > Threshold else DOWN if Slope < -Threshold else NEUTRAL`
- **Inputs:** `TrendSlopeEvidence`, `VolatilityEvidence` (for dynamic Thresholds)
- **Complexity:** `O(1)` streaming.

## 3. Strength Engine
### Strength Measurement
- **Formula:** Derived from directional momentum indicators stripped of semantic names (e.g., Average Directional Index (ADX) calculation math).
  - `+DM = max(High_t - High_{t-1}, 0)` (if > `Low_{t-1} - Low_t`)
  - `-DM = max(Low_{t-1} - Low_t, 0)` (if > `High_t - High_{t-1}`)
  - `DX = 100 * abs(+DI - -DI) / (+DI + -DI)`
  - `Strength = EMA(DX)`
- **Inputs:** OHLCV, `VolatilityEvidence` (ATR).
- **Complexity:** `O(1)` streaming.

## 4. State Engine
### Structural State
- **Formula:** 
  - `Impulse`: `Strength > Threshold` AND `Accel * Slope > 0`
  - `Correction`: `Strength > Threshold` AND `Accel * Slope < 0`
  - `Expansion`: `VolatilityRegime == 'Expanding'`
  - `Compression`: `VolatilityRegime == 'Contracting'`
  - `Consolidation`: `Strength < Threshold` AND `Direction == NEUTRAL`
  - `Transition`: `Direction_t != Direction_{t-1}`
- **Inputs:** `TrendStrengthEvidence`, `TrendGeometryEvidence`, `VolatilityEvidence`
- **Complexity:** `O(1)` streaming.

## 5. Persistence Engine
### Persistence Duration
- **Formula:** Count of consecutive periods where `Direction` remains unchanged.
- **Inputs:** `TrendDirectionEvidence`
- **Complexity:** `O(1)` streaming.
