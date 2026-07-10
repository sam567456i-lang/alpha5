# Liquidity Level Rule Specification

| Field | Value |
| :--- | :--- |
| **Rule ID** | `LiquidityLevelRule` |
| **Version** | `v1.0.0` |
| **Author** | System |
| **Created** | 2026-07-10 |

## Objective
The LiquidityLevelRule transforms purely geometric structural pivots into active, tracked, objective price zones to measure whether resting liquidity is empirically accumulating at those locations.

## Observable Hypothesis (H1)
Unswept validated swing highs/lows identify price levels that are revisited at a rate greater than random structural levels within a defined time horizon, producing measurable reactive behavior.

## Mathematical Definition
- A `LiquidityLevel` is instantiated at the exact high/low price of a `ValidatedSwingEvidence`.
- A level remains `untouched` if the asset price does not penetrate the exact price coordinate.
- A level is updated with a `touch_count` increment and reactive tick calculation whenever price crosses the level.
- A level transitions to `swept` or `invalidated` depending on policy parameters (e.g., body closes beyond the level vs wicks).

## Inputs & Dependencies
- **Consumes**: `ValidatedSwingEvidence`, `Platform10.OHLC`
- **Dependencies Layer**: Primitive Layer (Consumes only measurements and sibling primitives)

## Outputs & Published Evidence
- **Publishes**: `LiquidityLevel`
- **Payload**: 
  - `uuid`: string
  - `reference_swing_uuid`: string
  - `price_level`: float
  - `creation_timestamp_ms`: int
  - `age_bars`: int
  - `touch_count`: int
  - `sweep_status`: string [UNTOUCHED, SWEPT, INVALIDATED]

## Ground Truth Labels (EXP-000002)
To empirically test Detection Quality against this rule, we assign labels as follows:
- **Positive Label**: Level remained untouched initially, was later revisited, AND produced at least X tick reaction within Y bars of the touch.
- **Negative Label**: Level was never revisited OR was broken immediately upon first revisit OR reaction was smaller than threshold X.

## Assumptions
- Assumes OHLC data granularity is sufficient to detect touches without deep tick-data reconstruction.
- Assumes that single-tick penetrations trigger the state machine logic without slippage distortion.

## Failure Modes
- **Phantom Liquidity**: Levels held for excessively long durations (e.g., years) may trigger false positives simply due to eventual mean reversion.
- **Data Gap Blindness**: Missing 1-minute OHLC bars could cause the rule to miss a touch or sweep.

## Computational Complexity
- **Time**: $O(1)$ constant time evaluation per new OHLC bar to check against active levels.
- **Space**: $O(M)$ where $M$ is the number of currently active/uninvalidated liquidity levels in memory.

## Conditions for Disproval (Falsifiability)
This hypothesis is considered disproven if the Precision (correct identification of reactive levels) falls below 0.88, or if the False Positive Rate exceeds 0.15, indicating the levels possess no greater predictive power than randomly drawn horizontal lines.

## Validation & Version History
- **v1.0.0**: Initial specification drafted.
