---
Authority: Level 1
Parent: Docs/Governance/Constitution.md
Children: None
Supersedes: None
Version: 1.0.0
Status: ACTIVE
---

# Cross-Cutting Services (Layer 4)

These services are shared utilities consumed across multiple Platforms and Programs. They are never isolated islands.

## 1. Statistical Validation Service
- **Purpose:** Rigorous institutional validation of decisions and strategies.
- **Components:** Bootstrap, Monte Carlo, Walk Forward, CSCV, White Reality Check, Deflated Sharpe.
- **Consumers:** Platform 14 (Learning), Research Platform, Platform 12 (Decision).

## 2. Strategy Governance Service
- **Purpose:** Lifecycle management for AlphaGrid strategies.
- **Components:** Strategy Versioning, Validation Pipeline, Approval Gates, Retirement.
- **Consumers:** Platform 12 (Decision), Research Platform.

## 3. Risk Service
- **Purpose:** Strictly enforce downside boundaries mathematically.
- **Components:** VaR, MAE, MFE, Drawdown Limits, Position Risk constraints.
- **Consumers:** Platform 12 (Decision Support), Platform 13 (Execution).

## 4. Portfolio Intelligence
- **Purpose:** Manage global capital allocations and systemic risk across concurrent strategies.
- **Components:** Correlation matrices, Sector Exposure, Dynamic Capital Allocation, Hedging overlays.
- **Consumers:** Platform 12 (Decision Support), Platform 13 (Execution).

## 5. Simulation Service
- **Purpose:** Provide ultra-realistic offline replay environments.
- **Components:** Market Simulator, Broker Simulator, Latency/Slippage/Spread Simulators.
- **Consumers:** Platform 13 (Execution testing), Research Platform.

## 6. Performance Engineering
- **Purpose:** Track the underlying hardware efficiency of the pipeline.
- **Components:** CPU profiling, Memory bounds, DAG optimization, Latency Benchmarks.
- **Consumers:** Operations Platform, Developer Platform.
