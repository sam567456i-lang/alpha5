---
Authority: Level 1
Parent: Docs/Governance/Constitution.md
Type: Data Matrix
Status: FROZEN
Version: 1.0.0
---

# Platform 10 Data Availability Matrix

This matrix governs the strict relationship between Platform 10 capability families and raw data constraints. It dictates how each family degrades when required data is unavailable, ensuring that the architecture can safely adapt to lower-tier data feeds.

## Core Matrix

| Capability Family | OHLC | Volume | Tick Data | Level II | MBO | Multi-Symbol | Optional Feeds | Degradation Path (If Unavailable) |
|---|---|---|---|---|---|---|---|---|
| **Statistics** | Required | Optional | — | — | — | — | Open Interest | Works without Volume. |
| **Trend** | Required | Optional | — | — | — | — | — | Works without Volume. |
| **Swing** | Required | — | — | — | — | — | — | Fully Supported. |
| **Range** | Required | — | — | — | — | — | — | Fully Supported. |
| **Geometry** | Required | — | — | — | — | — | — | Fully Supported. |
| **Liquidity Objects** | Required | Optional | — | — | — | — | — | Fully Supported (Volume aids confidence score). |
| **Liquidity Events** | Required | Optional | — | — | — | — | — | Fully Supported (Volume aids confidence score). |
| **Structure Objects**| Required | — | — | — | — | — | — | Fully Supported. |
| **Structure Events** | Required | Optional | — | — | — | — | — | Fully Supported. |
| **Institutional Zones**| Required | Optional | — | — | — | — | — | Fully Supported. |
| **Imbalance Objects**| Required | Optional | — | — | — | — | — | Fully Supported. |
| **Imbalance Events** | Required | Optional | — | — | — | — | — | Fully Supported. |
| **Volume Analytics** | Required | Required | Optional | — | — | — | Tick Volume | Falls back to OHLC-inferred volume proxies if missing. |
| **Volume Profile** | Required | Required | Required | — | — | — | Trade Data | *Without Tick:* Falls back to Approximation Mode (TPO). |
| **Auction Market** | Required | Required | Required | — | — | — | — | *Without Volume Profile:* Disabled. |
| **Order Flow** | Required | Required | Required | Required | Required | — | Footprints | *Without L2/MBO:* Disabled (Remains Designed). |
| **Price Action** | Required | — | — | — | — | — | — | Fully Supported. |
| **Pattern Rec.** | Required | — | — | — | — | — | — | Fully Supported. |
| **Momentum** | Required | Optional | — | — | — | — | — | Fully Supported. |
| **Mean Reversion** | Required | Optional | — | — | — | — | — | Fully Supported. |
| **Wyckoff Evidence** | Required | Required | — | — | — | — | — | *Without Volume:* Approximation Mode. |
| **Cross Market** | Required | — | — | — | — | Required | Correlation Feeds | *Without Multi-Symbol:* Disabled. |
| **Feature Eng.** | Required | Required | — | — | — | — | — | Degrades gracefully based on upstream family availability. |
