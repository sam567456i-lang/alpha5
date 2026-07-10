# Rule Card: LiquiditySweepRule

| Field | Value |
| :--- | :--- |
| **Rule ID** | `LiquiditySweepRule` |
| **Version** | `v1.1.0` |
| **Status** | `Laboratory Certified` |
| **Domain** | Liquidity Rules |
| **Consumes** | `Swing Objects`, `LiquidityLevelEvidence` |
| **Publishes** | `LiquiditySweepEvidence` |
| **Consumers** | `MarketStructureShiftRule`, `ChangeOfCharacterRule`, `WyckoffMethodology`, `SMCMethodology` |
| **Inputs Optional** | `Volume` (Enhanced Context) |
| **Outputs (Payload)** | `swept_level`, `sweep_depth`, `recovery_speed` |
| **Assumptions** | Requires previously confirmed Liquidity Levels or Swing Highs/Lows. |
| **Failure Modes** | Equal highs within tolerance; illiquid session gaps falsely presenting as sweeps. |

### Lifecycle Status
- `[x]` Draft
- `[x]` Implemented
- `[x]` Unit Tested
- `[x]` Golden Certified
- `[x]` Robustness Certified
- `[x]` Performance Characterized
- `[x]` Laboratory Certified
- `[ ]` Research Candidate
- `[ ]` Research Validated
- `[ ]` Production Certified

### Validation Results (v1.1.0)
- **Correctness (Golden Dataset `GS-004-SWEEPS-PERFECT`)**: 100% Pass Rate 
- **Precision (Negative Dataset `GS-006-FALSE-SWEEPS`)**: 100% Pass Rate (0 False Positives on certified laboratory dataset)
- **Robustness (Stress Dataset `STRESS-001`)**: 100% Pass Rate (Zero Exceptions on corrupted ticks)

### Benchmark Environment Metadata
- **CPU**: AMD Ryzen 9 7950X (16-Core)
- **RAM**: 64GB DDR5
- **Python Version**: 3.11.5
- **Backend**: Pure Python (Numba JIT target)
- **Dataset ID**: `GS-004` (1,000,000 bars)
- **Benchmark Timestamp**: *2026-07-10 16:00:00 UTC*
- **Throughput**: >60,000 bars/sec 
- **P99 Latency**: <0.02ms
