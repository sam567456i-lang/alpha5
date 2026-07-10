# EXP-SENS-5: Detection Quality
*Machine-Generated Execution Summary*

## Immutable Descriptor
```json
{
  "ExperimentID": "EXP-SENS-5",
  "DatasetPath": "Backend/core/research/data/WF-BTCUSDT-2024Q1.csv",
  "RuleConfig": {
    "WindowBars": 11
  },
  "LabelPolicy": {
    "Type": "ATR_MULTIPLIER",
    "ATRLength": 21,
    "Multiplier": 3.0,
    "ReactionWindow": 20
  },
  "CodeCommit": "HEAD"
}
```

## Global Confusion Matrix
| TP | FP | TN | FN |
|---|---|---|---|
| 44 | 89 | 1788 | 233 |

**Metrics**: Precision: 33.08%, Recall: 15.88%, F1: 21.46%

## Label Statistics
- **Positive Rate**: 12.68%
- **Negative Rate**: 87.32%
- **Average Reaction Size**: $1057.53
- **Median Reaction Size**: $648.72
- **Detection Delay**: 5.5 bars

## Regime Breakdown
| Regime | TP | FP | FN | Precision | Recall | F1 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Trending** | 38 | 84 | 195 | 31.15% | 16.31% | 21.41% |
| **Ranging** | 6 | 5 | 38 | 54.55% | 13.64% | 21.82% |
