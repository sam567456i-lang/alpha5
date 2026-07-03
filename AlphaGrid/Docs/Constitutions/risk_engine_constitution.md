---
Document ID: CONST-007
Title: "Risk Engine Constitution"
Version: 1.0.0
Governance Version: 1.0.0
Architecture Version: 1.0.0
Phase: 10
Owner: ArchitectureTeam
Category: Constitutions
Maturity: "Level 5: Institutionally Frozen"
Implementation Status: Validated
Current Phase: 10
Future Phase: N/A
Last Validated Phase: 10
Review Date: 2026-07-03
Dependencies: []
Referenced By: []
---

# Risk Engine Constitution

## 1. Purpose
Defines the absolute boundaries and rules for the Risk Engine, which serves as the final barrier between a theoretical Strategy Decision and an actual Execution Plan.

## 2. Scope
- Trade Risk (Position level sizing and stops)
- Portfolio Risk (Aggregate exposure and correlations)
- Capital & Margin Management
- System-Wide Kill Switches

## 3. Responsibilities
- Receives `DecisionDTO` from the Strategy Engine.
- Outputs `RiskDecisionDTO` (Approved, Modified, or Rejected).
- Strictly prevents catastrophic capital loss.

## 4. Architecture
*(To be populated in Phase 13)*

## 5. DTOs
- `DecisionDTO`
- `RiskDecisionDTO`
- `ExposureSnapshotDTO`

## 6. Interfaces
- `IRiskEvaluator`
- `IPortfolioManager`
- `IKillSwitchDetector`

## 7. Dependencies
- Depends on `DecisionDTO`.
- Does NOT depend on Strategy or Features directly.

## 8. Runtime
### 8.1 Trade Risk
Must evaluate: Stop Loss, Take Profit, Trailing Stops, ATR, Volatility, Liquidity.
### 8.2 Portfolio Risk
Must evaluate: Correlation, Beta, Value-at-Risk (VaR), Expected Shortfall, Factor Exposure, Concentration, Leverage.
### 8.3 Capital
Must evaluate: Capital Allocation, Reserves, Drawdown Budgets, Exposure Budgets.
### 8.4 Kill Switches
Must hard-stop trading upon: Broker failure, Exchange outage, Latency spikes, Extreme Volatility, Connectivity loss, Data Quality degradation.

## 9. Validation
- Must be mathematically verified via Monte Carlo simulations of the risk constraints.

## 10. Failure Modes
- If Risk Engine crashes, all active trading HALTS immediately. Kill switch engaged.

## 11. Metrics
- Capital Utilization %
- Margin Utilization %
- Rejection Rate

## 12. Extension Points
- Custom `IRiskEvaluator` plugins for new asset classes.

## 13. References
- See Institutional Risk Models literature.

## 14. Cross-links
- Related ADRs: TBD
- Related RFCs: TBD
- Related Specs: `dto_specification.md`
- Related Reviews: `Risk Engine Review`
- Related Roadmap: Phase 13
