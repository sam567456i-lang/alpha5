# Swing Validation Rule Specification

| Field | Value |
| :--- | :--- |
| **Rule ID** | `SwingValidationRule` |
| **Version** | `v1.0.0` |
| **Author** | System |
| **Created** | 2026-07-10 |

## Objective
The SwingValidationRule acts as a mathematical filter over raw Platform 10 Swing measurements. It validates whether a purely mathematical swing extreme possesses the minimum geometry required to be considered a statistically significant structural pivot.

## Mathematical Definition
A Swing High $S_H$ is considered structurally valid if and only if:
1. The difference between $S_H$ and the preceding Swing Low $S_{L(-1)}$ exceeds the configured minimum ATR expansion threshold ($E_{min}$).
2. The number of bars between $S_{L(-1)}$ and $S_H$ exceeds the minimum time duration ($T_{min}$).
3. The peak is not mathematically subsumed by a larger overarching swing leg (complex pullbacks).

## Inputs & Dependencies
- **Consumes**: `Platform10.SwingObjects`, `Platform10.OHLC`, `Platform10.ATR`
- **Dependencies Layer**: None (Primitive Rule)

## Outputs & Published Evidence
- **Publishes**: `ValidatedSwingEvidence`
- **Payload**: `swing_uuid`, `swing_type` (HIGH/LOW), `amplitude_atr`, `duration_bars`, `validation_quality` (0.0 to 1.0)

## Assumptions
- Assumes Platform 10 emits raw pivots without attempting to gauge their overarching structural significance.
- Assumes the ATR measurement is synchronized to the same timeframe resolution as the Swing measurement.

## Failure Modes
- **Extreme Volatility Distortion**: In highly volatile regimes (e.g., news spikes), a single bar can exceed the amplitude threshold, causing a single wick to be incorrectly validated as a multi-bar structural swing leg.
- **Creeping Trends**: Slow, low-volatility grinds may fail to meet the amplitude threshold despite being universally recognized as structural swings by human analysts.

## Computational Complexity
- **Time**: $O(1)$ per new Swing object from Platform 10.
- **Space**: $O(N)$ where $N$ is the lookback window of unvalidated swings held in memory.

## Conditions for Disproval (Falsifiability)
This hypothesis is considered disproven if the `ValidatedSwingEvidence` outputs demonstrate zero predictive separation (in terms of future price confinement) compared to the raw unvalidated `Platform10.SwingObjects`. If validating swings provides no statistical advantage over using every raw pivot, the rule will be Rejected.

## Validation & Version History
- **v1.0.0**: Initial specification drafted.
