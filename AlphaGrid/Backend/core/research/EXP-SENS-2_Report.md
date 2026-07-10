# EXP-SENS-2: Detection Quality
*Machine-Generated Execution Summary*

## Immutable Descriptor
```json
{
  "ExperimentID": "EXP-SENS-2",
  "DatasetPath": "Backend/core/research/data/WF-BTCUSDT-2024Q1.csv",
  "RuleConfig": {
    "WindowBars": 11
  },
  "LabelPolicy": {
    "Type": "ATR_MULTIPLIER",
    "ATRLength": 21,
    "Multiplier": 1.0,
    "ReactionWindow": 20
  },
  "CodeCommit": "HEAD"
}
```

## Global Confusion Matrix
| TP | FP | TN | FN |
|---|---|---|---|
| 99 | 34 | 1270 | 751 |

**Metrics**: Precision: 74.44%, Recall: 11.65%, F1: 20.14%

## Label Statistics
- **Positive Rate**: 38.90%
- **Negative Rate**: 61.10%
- **Average Reaction Size**: $1057.53
- **Median Reaction Size**: $648.72
- **Detection Delay**: 1.4 bars

## Regime Breakdown
| Regime | TP | FP | FN | Precision | Recall | F1 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Trending** | 90 | 32 | 688 | 73.77% | 11.57% | 20.00% |
| **Ranging** | 9 | 2 | 63 | 81.82% | 12.50% | 21.69% |
