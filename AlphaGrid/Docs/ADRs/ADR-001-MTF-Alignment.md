---
Document ID: ADR-001
Title: "ADR-001: Multi-Timeframe (MTF) Alignment & Deterministic Evaluation"
Version: 1.0.0
Governance Version: 1.0.0
Architecture Version: 1.0.0
Phase: 10
Owner: ArchitectureTeam
Category: ADRs
Maturity: "Level 5: Institutionally Frozen"
Implementation Status: Validated
Current Phase: 10
Future Phase: N/A
Last Validated Phase: 10
Review Date: 2026-07-03
Dependencies: []
Referenced By: []
---

# ADR-001: Multi-Timeframe (MTF) Alignment & Deterministic Evaluation

## Status
**Approved** & **Immutable**

## Context
One of the most catastrophic failures in quantitative research is "look-ahead bias" introduced during multi-timeframe analysis. When a strategy running on a 5-minute chart queries a 4-hour or Daily chart for trend confirmation, it is common for research frameworks to accidentally provide the *current forming bar* (which includes future data relative to the 5-minute timestamp) rather than the *last fully closed bar*.

Furthermore, inconsistencies between how the Research environment (historical backtesting) and Live environment (real-time stream) align these timestamps inevitably lead to performance drift, where backtested results cannot be replicated in live trading.

## Decision
AlphaGrid mandates absolute determinism and zero look-ahead bias across all multi-timeframe aggregations. The following rules are now immutable architectural contracts:

### 1. Closed-Bar Only Rule
Higher timeframe bars are **closed bars only**. A lower timeframe may NEVER access the forming/unclosed higher timeframe bar for signal generation. 
- Example: At 10:15 AM, a 5-minute strategy querying a 1-hour bar will receive the finalized `09:00 - 10:00` bar. It will NOT receive any data from the forming `10:00 - 11:00` bar.

### 2. Environment Parity Rule
Live and Research environments must use the identical alignment rule. 
- In Research, MTF data is strictly joined via "as of" (forward-fill) logic using the closing timestamp of the higher timeframe bar against the closing timestamp of the lower timeframe bar.
- In Live, the state manager only broadcasts a higher timeframe update when the session clock passes the exact closing boundary.

### 3. Missing Bar Behavior (Forward-Fill)
If a higher timeframe bar is missing (e.g., due to exchange data issues or illiquidity), the system must safely forward-fill the last known closed bar. It must NEVER interpolate or drop the lower timeframe bars that attempt to align with it.

### 4. Session Boundary Truncation
Session boundaries forcefully truncate MTF aggregations. 
- Example: If the Indian Market (NSE) closes at 15:30, a 4-Hour bar starting at 13:15 must explicitly close at 15:30. It does NOT bleed into the next trading day. 

### 5. Alignment Timestamps
All alignment logic must evaluate based on the `close_timestamp` of the bar, never the `open_timestamp`.

## Consequences
- **Positive:** Absolute guarantee against MTF look-ahead bias. 100% parity between Research and Live pipeline execution.
- **Negative:** Strategies must be explicitly designed to trade on "lagging" MTF data (e.g., using yesterday's Daily close, or the previous Hour's close), which is realistic but occasionally frustrating to discretionary traders migrating to quant.

## Compliance
Any module, feature, or signal utilizing the `MultiTimeframeAlignmentEngine` that attempts to access a forming bar will fail the **Mathematical Verification Contract** and be rejected by the Production Acceptance Gate.
