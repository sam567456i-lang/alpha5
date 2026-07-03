---
Document ID: ADR-002
Title: "ADR-003: Ownership of expected_bars"
Version: 1.0.0
Governance Version: 1.0.0
Architecture Version: 1.0.0
Phase: 10
Owner: ArchitectureTeam
Category: ADRs
Maturity: "Level 5: Institutionally Frozen"
Implementation Status: Validated
Current Phase: 10
Future Phase: N/A
Last Validated Phase: 10
Review Date: 2026-07-03
Dependencies: []
Referenced By: []
---

# ADR-003: Ownership of expected_bars

## Status
Accepted

## Context
During canonical production pipeline recovery (Execution #016), the `DataQualityGate` was formally identified as the immediate downstream consumer of normalized OHLCV data. 

To execute its data quality evaluation, `DataQualityGate.evaluate_and_enforce` mathematically requires a parameter called `expected_bars`. A rigorous repository investigation proved that:
1. `expected_bars` exists only in the `DataQualityGate` signature.
2. No implementation of `calculate_expected_bars` exists anywhere in the repository.
3. The architecture documentation (`architecture_bible.md`) does not formally assign ownership of this calculation.

Because repository evidence could not prove an owner, the recovery protocol dictated a formal halt. We must now transition from "repository recovery" to "architecture completion" to establish this ownership.

## Alternatives Considered

### A. SessionEngine
`SessionEngine` currently manages market sessions, exchange hours, trading windows, and session timing. Because expected bar counts are intrinsically derived from trading sessions and exchange hours, it is structurally cohesive to calculate them here.

### B. TradingCalendar
`TradingCalendar` manages holiday rules and expiry resolution. While relevant for determining *if* a day is active, it lacks the intraday timing precision required to count bars for varying timeframes (e.g., 1m, 1h).

### C. ExchangeContract
The contract defines the hours, but is a static data structure rather than an active computation engine.

### D. New MarketCalendarService
A net-new service dedicated solely to bar calculation. Rejected as unnecessarily increasing the surface area of the domain.

## Decision
We choose **Alternative A: SessionEngine**.

`SessionEngine` is formally designated as the architectural owner of `calculate_expected_bars`.

## Consequences
- `SessionEngine` will expose a new method: `calculate_expected_bars(start_time: datetime, end_time: datetime, timeframe: str) -> int`.
- The `MarketService` (API Orchestrator) will consume this method to satisfy the `DataQualityGate` contract without intentionally violating its interface.
