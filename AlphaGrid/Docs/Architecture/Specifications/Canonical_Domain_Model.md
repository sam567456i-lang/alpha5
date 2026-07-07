# Canonical Domain Model Specification
*AlphaGrid Mandatory Infrastructure Framework 1/5*

This specification defines the universal language for all AlphaGrid objects. Every DTO extending across platform boundaries must conform strictly to these metadata requirements.

## 1. Universal Base Object (DomainEntity)
Every major object in the system MUST inherit from a frozen, immutable base containing:

* **Identity**: UUIDv4 (`id`)
* **Timestamp**: UTC creation time (`created_at`)
* **Lifecycle**: E.g., `PENDING`, `EVALUATED`, `CERTIFIED`, `REJECTED`, `EXECUTED`
* **Version**: Schema version tracking (e.g., `v1.0`)
* **Owner**: The exact platform or plugin that generated the object.
* **Traceability**: An ordered list/DAG of parent UUIDs (`provenance_chain`).
* **Confidence**: Deterministic float [0.0, 1.0] indicating data quality or statistical weight.
* **Fingerprint**: SHA256 hash of the object's immutable fields.

## 2. Shared Business Objects

### 2.1 Market & Asset Hierarchy
* **Market**: (e.g., `NASDAQ`, `CME`) Owns trading calendars, session definitions, and settlement rules.
* **Asset**: (e.g., `AAPL`, `ES`) Base entity containing static metadata (Tick size, margins, multiplier).
* **Instrument**: The tradable instance (e.g., `ESM6`).

### 2.2 Time Series Hierarchy
* **Tick**: Raw L1/L2 data point.
* **Candle**: Aggregated OHLCV with explicit `timeframe` and `alignment_rule`.
* **Feature**: A computed mathematical derivative over a Time Series (e.g., `RSI_14`).
* **Concept**: A boolean or categorical human-readable market state (e.g., `BOS_Bullish`).

### 2.3 Decision Pipeline Hierarchy
* **Signal**: A standardized directional intent emitted by a methodology plugin.
* **Opportunity**: A localized, multi-signal structure clustered on a specific asset/timeframe.
* **Recommendation**: A fully validated, conflict-resolved Opportunity awaiting Risk approval.
* **Risk Assessment**: Output of Platform 15 determining sizing, exposure safety, and capital limit enforcement.
* **Portfolio Assessment**: Output of Platform 16 evaluating correlation, concentration, and net delta.

## 3. Relationships & Provenance
A `Recommendation` cannot exist without an `Opportunity`. 
An `Opportunity` cannot exist without `Signals`. 
All objects must maintain absolute traceability back to the exact `Market State` object that originated them.
