# EXP-SENS-3: Detection Quality
*Machine-Generated Execution Summary*

## Immutable Descriptor
```json
{
  "ExperimentID": "EXP-SENS-3",
  "DatasetPath": "Backend/core/research/data/WF-BTCUSDT-2024Q1.csv",
  "RuleConfig": {
    "WindowBars": 11
  },
  "LabelPolicy": {
    "Type": "ATR_MULTIPLIER",
    "ATRLength": 21,
    "Multiplier": 1.5,
    "ReactionWindow": 20
  },
  "CodeCommit": "HEAD"
}
```

## Global Confusion Matrix
| TP | FP | TN | FN |
|---|---|---|---|
| 80 | 53 | 1488 | 533 |

**Metrics**: Precision: 60.15%, Recall: 13.05%, F1: 21.45%

## Label Statistics
- **Positive Rate**: 28.05%
- **Negative Rate**: 71.95%
- **Average Reaction Size**: $1057.53
- **Median Reaction Size**: $648.72
- **Detection Delay**: 2.3 bars

## Regime Breakdown
| Regime | TP | FP | FN | Precision | Recall | F1 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Trending** | 73 | 49 | 479 | 59.84% | 13.22% | 21.66% |
| **Ranging** | 7 | 4 | 54 | 63.64% | 11.48% | 19.44% |
