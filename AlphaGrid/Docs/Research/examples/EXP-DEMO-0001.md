## EXP-DEMO-0001 (ILLUSTRATIVE / HYPOTHETICAL)
*Note: This is an architectural simulation of a completed experiment. No real market data was processed.*

- **Hypothesis**: ATR-normalized swings (Amplitude > 1.5 ATR, Duration > 3 bars) provide a statistically significant improvement in structural precision over raw geometric pivots.
- **Target Rule**: `SwingValidationRule v1.0`
- **Result**: `Rejected (Hypothetical)`
- **Observation**: Falsified by simulated precision collapse in ranging markets (0.68), triggering the absolute Reject threshold (< 0.75).
- **Possible Explanations**: 
  - *H1*: ATR compresses in ranges, making the static 1.5 threshold too easy to hit.
  - *H2*: Pivot geometry alone is insufficient without volume confirmation.
  - *H3*: Ground-truth labels are biased toward trending environments.
- **Next Action**: Execute EXP-000002 to specifically test H1 (Adaptive Geometry Threshold).
- **Date**: 2026-07-10
