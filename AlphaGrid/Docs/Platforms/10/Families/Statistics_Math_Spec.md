---
Authority: Level 2
Parent: Docs/Platforms/10/Families/Statistics_Specification.md
Type: Mathematical Specification
Domain: Statistics
Platform: 10
Version: 1.0.0
Status: ACTIVE
CRL: CRL-2
---

# Statistics Family Mathematical Specification

This specification strictly documents the mathematical formulas, time complexities, and algorithmic properties of the Statistics engines.

## 1. Distribution Engine
### Mean
- **Formula:** `μ = (Σ x_i) / n`
- **Inputs:** `List[float]`
- **Complexity:** `O(n)` batch, `O(1)` streaming (Welford's algorithm)
- **Streaming Support:** Yes
- **Replay Determinism:** Guaranteed

### Variance & Standard Deviation
- **Formula:** `σ^2 = (Σ (x_i - μ)^2) / (n - 1)` (Sample Variance)
- **Inputs:** `List[float]`
- **Complexity:** `O(n)` batch, `O(1)` streaming (Welford's algorithm)
- **Numeric Stability:** Guard against catastrophic cancellation when variance is near zero.

## 2. Volatility Engine
### True Range (TR)
- **Formula:** `TR = max(High - Low, abs(High - PreviousClose), abs(Low - PreviousClose))`
- **Inputs:** `High`, `Low`, `Close (t-1)`
- **Complexity:** `O(1)` per bar
- **Numeric Stability:** Safe for constant prices (TR = 0).

### Average True Range (ATR)
- **Formula:** `ATR_t = (ATR_{t-1} * (n-1) + TR_t) / n` (RMA smoothing)
- **Inputs:** `TR` stream, period `n`
- **Complexity:** `O(n)` initial, `O(1)` streaming

## 3. Normalization Engine
### Z-Score
- **Formula:** `Z = (x - μ) / σ`
- **Inputs:** Current value `x`, Rolling Mean `μ`, Rolling StdDev `σ`
- **Complexity:** `O(1)` streaming
- **Edge Cases:** If `σ == 0`, `Z = 0`.

### Percentile Rank
- **Formula:** `%Rank = (Count of elements <= x) / Total Elements`
- **Inputs:** Value `x`, lookback window
- **Complexity:** `O(n log n)` batch, `O(log n)` streaming (using sorted structures or approximations like T-Digest)

## 4. Confidence Engine
### Confidence Interval (Mean)
- **Formula:** `CI = μ ± (Z * (σ / sqrt(n)))`
- **Inputs:** `μ`, `σ`, `n`, Critical Z-value (e.g., 1.96 for 95%)
- **Complexity:** `O(1)` streaming
