# Experiment Summary: EXP-000001 (ILLUSTRATIVE / HYPOTHETICAL)
*Note: This is an architectural simulation of a completed experiment. No real market data was processed.*

## Metadata
- **Experiment ID**: `EXP-000001`
- **Date Executed**: 2026-07-10
- **Target Rule**: `SwingValidationRule v1.0`
- **Objective Stage**: Detection Quality (EXP-1)
- **Dataset**: `WF-2024-Q1` (Labeled structural swings)
- **Asset**: BTCUSDT
- **Timeframe**: 1H

## Up-Front Promotion Criteria
- **Promote**: Precision ≥ 0.90, Recall ≥ 0.85, F1 ≥ 0.87, Delay ≤ 2 bars
- **Revise**: Precision ≥ 0.75 but fails Promote thresholds
- **Reject**: Precision < 0.75

## Empirical Results (Simulated)
We simulated executing `SwingValidationRule v1.0` (Amplitude > 1.5 ATR, Duration > 3 bars) across the `WF-2024-Q1` dataset. The ground truth was labeled using manual visual verification of major structural pivots.

### Trending Regime Performance (Simulated)
- **Precision**: 0.92
- **Recall**: 0.88
- **F1**: 0.90
- **Detection Delay**: 1.2 bars

### Ranging Regime Performance (Simulated)
- **Precision**: 0.68
- **Recall**: 0.94
- **F1**: 0.78
- **Detection Delay**: 1.4 bars

## Analysis & Verdict
While the rule performed exceptionally well during trending regimes, successfully filtering out minor pullbacks, the Precision collapsed catastrophically in Ranging regimes (0.68). 

**Observation:** In ranging markets, volatility contracts. The ATR value shrinks significantly. As price chops sideways, minor irrelevant wicks easily exceeded the compressed 1.5 ATR threshold, causing a flood of False Positives.

**Verdict: REJECT (Hypothetical)**
*Reason: Precision in ranging regimes (0.68) fell below the absolute minimum threshold of 0.75.*

## Possible Explanations & Next Actions
The observation that precision degraded in ranging markets due to ATR compression leads to the following potential hypotheses:
- **H1**: ATR compresses in ranges, making a static 1.5 threshold mathematically too easy to exceed.
- **H2**: Pivot geometry alone is insufficient for validation without volume confirmation.
- **H3**: Ground-truth labels in the dataset are biased toward trending environments.

**Next Experiment**: Execute `EXP-000002` to specifically test **H1** by replacing the local volatility calculation with an adaptive, macro-range geometry threshold.
