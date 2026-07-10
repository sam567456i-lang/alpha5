# EXP-000001: Detection Quality
*Machine-Generated Execution Summary & Research Report | Timestamp: 2026-07-10T13:13:53Z*

## Reproducibility & Configuration
- **Git Commit**: `c263658`
- **Python Version**: `3.11`
- **Dataset**: WF-Binance-9f08cf (Hash: 9f08cf5eff224a3a)
- **Rule Version**: LiquidityLevelRule v1.0.0
- **Configuration**: `CFG-0001` (11-bar Pivot High, $500 Reaction Threshold, 20-bar Window)

## Complete Confusion Matrix (Global)
| Metric | Value |
| :--- | :--- |
| **True Positives (TP)** | 82 |
| **False Positives (FP)** | 51 |
| **True Negatives (TN)** | 1413 |
| **False Negatives (FN)** | 608 |

## Evaluation Metrics
- **Precision**: 61.65%
- **Recall**: 11.88%
- **F1 Score**: 19.93%
- **Specificity**: 96.52%
- **Detection Delay**: 2.0 bars (avg time to reach $500 reaction)

## Regime Breakdown (Preliminary Stability - P3b)
| Regime | TP | FP | FN | Precision | Recall | F1 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Trending (High Vol)** | 30 | 18 | 260 | 62.50% | 10.34% | 17.75% |
| **Ranging (Low Vol)** | 52 | 33 | 348 | 61.18% | 13.00% | 21.44% |

## Formal Research Report (P4A)

### Assumptions
- A valid institutional liquidity reaction is defined as a $500 directional movement within 20 hours.
- A local maximum across an 11-bar window correctly isolates potential sell-side liquidity pools.

### Limitations & Threats to Validity
- **Dataset Limitation**: Only BTCUSDT 1H data was tested.
- **Labeling Sensitivity**: The $500 threshold is static. During low volatility regimes, this threshold may be impossible to hit, artificially suppressing True Positives.
- **Rule Simplicity**: The rule evaluates only 11 bars of price action.

### Conclusions
The rule achieves 61.65% precision but a severely degraded recall of 11.88%. The false positive rate remains substantial.

**Possible explanations requiring future testing:**
- **H1**: Volume confirmation reduces false positives.
- **H2**: Multi-timeframe alignment improves precision.
- **H3**: Static reaction thresholds are inappropriate across volatility regimes.

**Recommendation**: **REJECT**
The hypothesis that "11-bar pivot highs under CFG-0001 detect future $500 reactions on BTCUSDT 1H" is falsified. This does not disprove the overarching concept of liquidity levels, but strictly falsifies this specific, unmitigated implementation on this dataset.

**Next Action**: Proceed to P4B (Research Review) to diagnose whether the failure stems from the Rule implementation, the static $500 Label threshold, or the Experimental Design.
