# EXP-SENS-1: Detection Quality
*Machine-Generated Execution Summary*

## Immutable Descriptor
```json
{
  "ExperimentID": "EXP-SENS-1",
  "DatasetPath": "Backend/core/research/data/WF-BTCUSDT-2024Q1.csv",
  "RuleConfig": {
    "WindowBars": 11
  },
  "LabelPolicy": {
    "Type": "STATIC",
    "Threshold": 500.0,
    "ReactionWindow": 20
  },
  "CodeCommit": "HEAD"
}
```

## Global Confusion Matrix
| TP | FP | TN | FN |
|---|---|---|---|
| 82 | 51 | 1413 | 608 |

**Metrics**: Precision: 61.65%, Recall: 11.88%, F1: 19.93%

## Label Statistics
- **Positive Rate**: 31.58%
- **Negative Rate**: 68.42%
- **Average Reaction Size**: $1057.53
- **Median Reaction Size**: $648.72
- **Detection Delay**: 2.0 bars

## Regime Breakdown
| Regime | TP | FP | FN | Precision | Recall | F1 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Trending** | 76 | 46 | 578 | 62.30% | 11.62% | 19.59% |
| **Ranging** | 6 | 5 | 30 | 54.55% | 16.67% | 25.53% |
