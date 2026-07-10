# Rule Card: BreakOfStructureRule

| Field | Value |
| :--- | :--- |
| **Rule ID** | `BOSRule` |
| **Version** | `v1.0.0` |
| **Status** | `Laboratory Certified` |
| **Domain** | Structure Rules |
| **Required Data** | `OHLC` |
| **Required Objects** | `Swing Detection Objects (Platform 10)` |
| **Optional Data** | `None` |
| **Unsupported Data** | `Tick-only feeds` |
| **Outputs** | `RuleEvidence` (payload: `broken_swing_uuid`, `break_price`, `break_depth`, `confirmation_method`, `invalidation_level`) |
| **Assumptions** | Assumes the provided Swing objects have already been mathematically certified as valid structural extremes. |
| **Failure Modes** | Equal highs triggering a break by 1 tick (mitigated by `BOSPolicy.equal_high_tolerance_ticks`). |
| **Golden Dataset** | `GS-005-BOS-PERFECT` |
| **Negative Dataset** | `GS-006-BOS-FALSE-BREAKS` |
| **Last Validation** | *2026-07-10* |
| **Known Weaknesses** | Highly volatile wicks can trigger false positive BOS under `WICK` policy. |

### Laboratory Validation Results (v1.0.0)
- **Correctness (Golden)**: 100% Pass Rate
- **Precision (Negative Data)**: 100% Pass Rate (0 False Positives on Ranging/False Breakouts)
- **Robustness (Stress)**: 100% Pass Rate 
- **Throughput**: >150,000 bars/sec (Pure OHLC computation)
- **P99 Latency**: <0.01ms

*Approved by Automated Policy Engine*
