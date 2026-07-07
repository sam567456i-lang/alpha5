# Data Quality Framework Specification
*AlphaGrid Mandatory Infrastructure Framework 4/5*

Garbage data must not reach downstream geometries or features. The Data Quality Framework establishes a strict validation gate that executes *before* any feature calculation or market intelligence derivation.

## 1. Pre-Analytics Validation Rules
Before time-series data is released to the pipeline, the following exact checks must pass:

### 1.1 Temporal Integrity
* **Missing Data**: No null fields in High, Low, Open, Close, Volume.
* **Time Gaps**: Detection of unexpected gaps (e.g., missing 1-minute bars during active market hours).
* **Bad Timestamps**: Duplicate timestamps, unordered ticks, or timestamps occurring outside of valid exchange hours.

### 1.2 Price Integrity
* **Invalid OHLC**: `High < Low`, `Open < Low`, `Close > High` must immediately trigger a fatal validation error.
* **Outliers**: 3-sigma price spikes that revert entirely on the next tick must be flagged.

### 1.3 Corporate Action Integrity
* **Splits/Dividends**: Price data crossing a known split boundary must be backward-adjusted cleanly or rejected if adjustment meta-data is missing.

## 2. Error Taxonomy
The framework classifies errors rigidly.
* **Validation Error**: Bad input format or type.
* **Data Quality Error**: Logical data violation (e.g. Invalid OHLC).
* **Configuration Error**: Missing timeframe settings.

## 3. Downstream Confidence Propagation
Data Quality errors are not always fatal (e.g., a single missed tick). The framework calculates a `DataQualityConfidence` float [0.0, 1.0]. 
This confidence score travels via the canonical DTOs all the way to Platform 15 (Risk) and Platform 18 (Explainability), allowing risk sizing algorithms to penalize or reject recommendations built on low-quality data.
