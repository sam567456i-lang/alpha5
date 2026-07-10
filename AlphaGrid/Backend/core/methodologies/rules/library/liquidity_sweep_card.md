# Rule Card: LiquiditySweepRule

| Field | Value |
| :--- | :--- |
| **Rule ID** | `LiquiditySweepRule` |
| **Version** | `v1.0.0` |
| **Status** | `Validated` |
| **Domain** | Liquidity Rules |
| **Inputs Required** | `OHLC`, `Swing Detection Objects` |
| **Inputs Optional** | `Volume` (Enhanced Context) |
| **Outputs** | `RuleEvidence` (payload: `swept_level`, `sweep_depth`, `recovery_speed`) |
| **Assumptions** | Requires previously confirmed Swing Highs/Lows. |
| **Failure Modes** | Equal highs within tolerance; illiquid session gaps falsely presenting as sweeps. |
| **Golden Dataset** | `GS-004-SWEEPS-PERFECT` |
| **Walk-forward Dataset** | `WF-2022-ALL` |
| **Last Validation** | *2026-07-10* |
| **Known Weaknesses** | Low-liquidity chop ranges produce excessive false positives. |

### Validation Results (v1.0.0)
- **Correctness (Golden)**: 100% Pass Rate (0 False Positives)
- **Robustness (Stress)**: 100% Pass Rate (Zero Exceptions on corrupted ticks)
- **Throughput**: >60,000 bars/sec
- **P99 Latency**: <0.02ms

*Approved by Automated Policy Engine*
