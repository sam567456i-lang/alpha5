---
Document ID: GEN-179
Title: "Feature Catalog"
Version: 1.0.0
Governance Version: 1.0.0
Architecture Version: 1.0.0
Phase: 10
Owner: ArchitectureTeam
Category: Generated
Maturity: "Level 5: Institutionally Frozen"
Implementation Status: Validated
Current Phase: 10
Future Phase: N/A
Last Validated Phase: 10
Review Date: 2026-07-04
Dependencies: []
Referenced By: []
---

# AlphaGrid Feature Catalog

This catalog is auto-generated from the Feature Generator components.

| Feature Generator | Component ID Format | Interface | Dependencies |
|---|---|---|---|
| `ATRFeatureGenerator` | `ftr-atr-14-rma` | `VolatilityFeatureInterface` | `['ftr-ohlcv']` |
| `BollingerFeatureGenerator` | `ftr-bollinger-20-2.0` | `VolatilityFeatureInterface` | `['ftr-ohlcv']` |
| `EMAFeatureGenerator` | `ftr-ema-20` | `TrendFeatureInterface` | `['ftr-ohlcv']` |
| `KeltnerFeatureGenerator` | `ftr-keltner-20-10-2.0` | `VolatilityFeatureInterface` | `['ftr-ohlcv']` |
| `MACDFeatureGenerator` | `ftr-macd-12-26-9` | `TrendFeatureInterface` | `['ftr-ohlcv']` |
| `MACrossFeatureGenerator` | `ftr-ma-cross-ema10-ema30` | `TrendFeatureInterface` | `['ftr-ohlcv']` |
| `ROCFeatureGenerator` | `ftr-roc-14` | `FeatureInterface` | `['ftr-ohlcv']` |
| `SMAFeatureGenerator` | `ftr-sma-20` | `TrendFeatureInterface` | `['ftr-ohlcv']` |
| `WMAFeatureGenerator` | `ftr-wma-20` | `TrendFeatureInterface` | `['ftr-ohlcv']` |
