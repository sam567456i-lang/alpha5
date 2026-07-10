# EXP-000003: Detection Quality
*Machine-Generated Execution Summary*

## Immutable Descriptor
```json
{
  "ExperimentID": "EXP-000003",
  "DatasetPath": "Backend/core/research/data/WF-BTCUSDT-2024Q1.csv",
  "RuleConfig": {
    "WindowBars": 21
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
| 76 | 2 | 1452 | 614 |

**Metrics**: Precision: 97.44%, Recall: 11.01%, F1: 19.79%

## Label Statistics
- **Positive Rate**: 31.58%
- **Negative Rate**: 68.42%
- **Average Reaction Size**: $1057.53
- **Median Reaction Size**: $648.72
- **Detection Delay**: 2.0 bars

## Regime Breakdown
| Regime | TP | FP | FN | Precision | Recall | F1 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Trending** | 70 | 1 | 584 | 98.59% | 10.70% | 19.31% |
| **Ranging** | 6 | 1 | 30 | 85.71% | 16.67% | 27.91% |
