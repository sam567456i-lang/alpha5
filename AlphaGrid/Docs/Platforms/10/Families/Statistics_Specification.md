---
Authority: Level 2
Parent: Docs/AlphaGrid_Master_Roadmap.md
Type: Capability Family Specification
Domain: Statistics
Platform: 10
Version: 1.0.0
Status: ACTIVE
CRL: CRL-2 (Specification)
---

# Statistics Family Specification

**Family:** Statistics
**Owns:** ✓ Measurement, ✓ Quality
**Consumes:** ✓ Price, ✓ Time, ✓ Foundation
**Publishes:** ✓ VolatilityEvidence, ✓ DispersionEvidence, ✓ CorrelationEvidence
**Never Publishes:** ✗ Objects, ✗ Events, ✗ Trends, ✗ Methodology Terms

The **Statistics Family** is the foundational mathematical bedrock of Platform 10. Nearly all downstream capabilities (Trend, Volatility, Liquidity, Structure) depend on these objective measurements.

## 1. Domain Constraints
- **Strictly Objective:** This family must compute purely mathematical properties of the price/volume time series.
- **No Interpretations:** The Statistics family shall never emit signals, sentiment, or labels like "Accumulation" or "Bullish". It only emits measurements (e.g., `ZScore = 2.4`, `ATR = 15.5`).
- **Indicator Agnosticism:** Downstream consumers interact with `VolatilityEvidence` or `DistributionEvidence`, not explicit indicator objects like `EMA50Evidence`.

## 2. Capability Nodes
The family is decomposed into the following autonomous engines, each with its own test suite and lifecycle:

1. **Distribution Engine:** Computes Mean, Median, Mode, Variance, Standard Deviation, Skewness, Kurtosis, Entropy.
2. **Rolling Engine:** Computes rolling window versions (Rolling Mean, Rolling Median, Rolling Variance).
3. **Normalization Engine:** Computes Z-Score, Robust Z-Score, Min-Max, Rank Normalization, Percentiles, Quantiles, Deciles.
4. **Volatility Engine:** Computes ATR, True Range, Historical Volatility, Parkinson, Garman-Klass, Rogers-Satchell, Volatility Regimes (Expanding/Contracting).
5. **Confidence Engine:** Computes Confidence Intervals, Confidence Bands.
6. **Drift Engine:** Computes Distribution Drift, Variance Drift.
7. **Quality Engine:** Assesses the statistical quality/stationarity of the time series.

## 3. Downstream Consumers
- **Platform 10 Trend Family:** Depends heavily on Volatility and Rolling Statistics.
- **Platform 10 Market Structure Family:** Depends on Volatility regimes to define swing thresholds.
- **Platform 10 Liquidity Family:** Depends on Normalization to rank liquidity pool significance.
- **Platform 11 Profiles:** All profiles rely on standard deviation and ATR for stops/targets.

## 4. Certification Gates
This family cannot be marked complete until all engines pass the 19-step standard execution lifecycle, culminating in a `Statistics_Certification.md` report.
