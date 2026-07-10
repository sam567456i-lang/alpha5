# AlphaGrid Experiment Ledger

This ledger is a permanent, immutable record of all completed empirical experiments. It ensures that the project learns from its failures and prevents the resurrection of statistically disproven ideas.

*Research artifacts are immutable. Corrections create new versions; they do not overwrite historical records.*

---

## EXP-000001 [PENDING EXECUTION]

### Immutable Identifiers
- **Experiment ID**: `EXP-000001`
- **Rule Version**: `LiquidityLevelRule v1.0`
- **Specification Version**: `1.0`
- **Platform Version**: `Platform10 v1.0`
- **Dataset Version**: `WF-2024-Q1 v3`
- **Configuration Version**: `CFG-0001`

### Hypothesis
- **H0 (Null Hypothesis)**: Liquidity levels perform no better than random horizontal levels at predicting reactive price behavior.
- **H1 (Alternative Hypothesis)**: Unswept validated swing highs/lows identify price levels that are revisited at a rate greater than a randomized baseline, producing measurable reactive behavior.

### Experiment
- **Baseline Definition**: Random horizontal price levels sampled uniformly from the observed price range across the identical time horizon.
- **Configuration (`CFG-0001`)**: 
  - `reaction_ticks = 8`
  - `reaction_window = 20 bars`
  - `minimum_touch_separation = 5 bars`
- **Ground Truth Labels**:
  - *Positive*: Level remained untouched, was later revisited, AND produced at least `reaction_ticks` reaction within `reaction_window`.
  - *Negative*: Level never revisited OR broken immediately OR reaction < `reaction_ticks`.

### Metrics & Decision
- **Promotion Criteria**: Precision ≥ 0.88, Recall ≥ 0.85, False Positive Rate < 0.15.
- **Required Reporting**: Positive label frequency, Predicted positive frequency, Performance by regime, Calibration error.
- **Recommendation**: `[Pending Execution]`

### Execution Environment
- **Python**: `[Pending]`
- **OS**: `[Pending]`
- **CPU**: `[Pending]`
- **RAM**: `[Pending]`
- **Git Commit**: `[Pending]`

### Threats to Validity
- Single asset evaluation (BTCUSDT).
- Single timeframe evaluation (1H).
- Limited sample size of the dataset.
- Does not account for slippage or Level II depth.
