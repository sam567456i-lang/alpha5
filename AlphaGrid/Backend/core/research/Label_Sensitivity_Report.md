# Label Sensitivity Study (Phase A)

| Experiment | Threshold Policy | Precision | Recall | F1 | Total Positives |
|---|---|---|---|---|---|
| EXP-SENS-1 | Static $500 | 61.65% | 11.88% | 19.93% | 690 |
| EXP-SENS-2 | ATR(21) x 1.0 | 74.44% | 11.65% | 20.14% | 850 |
| EXP-SENS-3 | ATR(21) x 1.5 | 60.15% | 13.05% | 21.45% | 613 |
| EXP-SENS-4 | ATR(21) x 2.0 (CFG-LABEL-001) | 46.62% | 13.93% | 21.45% | 445 |
| EXP-SENS-5 | ATR(21) x 3.0 | 33.08% | 15.88% | 21.46% | 277 |

## Transition Matrices (vs Static $500)

### EXP-SENS-2 (ATR(21) x 1.0)
| Transition | Count |
|---|---|
| Pos->Pos | 629 |
| Pos->Neg | 61 |
| Neg->Pos | 221 |
| Neg->Neg | 1274 |

### EXP-SENS-3 (ATR(21) x 1.5)
| Transition | Count |
|---|---|
| Pos->Pos | 533 |
| Pos->Neg | 157 |
| Neg->Pos | 80 |
| Neg->Neg | 1415 |

### EXP-SENS-4 (ATR(21) x 2.0 (CFG-LABEL-001))
| Transition | Count |
|---|---|
| Pos->Pos | 422 |
| Pos->Neg | 268 |
| Neg->Pos | 23 |
| Neg->Neg | 1472 |

### EXP-SENS-5 (ATR(21) x 3.0)
| Transition | Count |
|---|---|
| Pos->Pos | 269 |
| Pos->Neg | 421 |
| Neg->Pos | 8 |
| Neg->Neg | 1487 |

