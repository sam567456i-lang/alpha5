# EXP-SENS-4: Detection Quality
*Machine-Generated Execution Summary*

## Immutable Descriptor
```json
{
  "ExperimentID": "EXP-SENS-4",
  "DatasetPath": "Backend/core/research/data/WF-BTCUSDT-2024Q1.csv",
  "RuleConfig": {
    "WindowBars": 11
  },
  "LabelPolicy": {
    "Type": "ATR_MULTIPLIER",
    "ATRLength": 21,
    "Multiplier": 2.0,
    "ReactionWindow": 20
  },
  "CodeCommit": "HEAD"
}
```

## Global Confusion Matrix
| TP | FP | TN | FN |
|---|---|---|---|
| 62 | 71 | 1638 | 383 |

**Metrics**: Precision: 46.62%, Recall: 13.93%, F1: 21.45%

## Label Statistics
- **Positive Rate**: 20.37%
- **Negative Rate**: 79.63%
- **Average Reaction Size**: $1057.53
- **Median Reaction Size**: $648.72
- **Detection Delay**: 3.4 bars

## Regime Breakdown
| Regime | TP | FP | FN | Precision | Recall | F1 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Trending** | 56 | 66 | 337 | 45.90% | 14.25% | 21.75% |
| **Ranging** | 6 | 5 | 46 | 54.55% | 11.54% | 19.05% |
