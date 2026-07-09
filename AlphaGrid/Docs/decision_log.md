---
Document ID: DOC-003
Title: "Decision Log"
Version: 1.0.0
Governance Version: 1.0.0
Architecture Version: 1.0.0
Phase: 10
Owner: ArchitectureTeam
Category: Root
Maturity: "Level 5: Institutionally Frozen"
Implementation Status: Validated
Current Phase: 10
Future Phase: N/A
Last Validated Phase: 10
Review Date: 2026-07-03
Dependencies: []
Referenced By: []
---

# Decision Log

## 1. Purpose
Provides a chronological, searchable ledger of *when* and *who* made major architectural decisions. (For the *why*, see the specific ADR).

## 2. Ledger

| Date | Decision | Owner | Outcome | Affected Docs | ADR Reference |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 2026-07-03 | Migrate Governance to Institutional standard | Platform Eng | Approved | All Docs | N/A |
| 2026-07-03 | Require Hash Gates for Migration | Platform Eng | Approved | Migration Framework | N/A |
| 2026-07-03 | Enforce Templates-Now-Depth-Later principle | ARB | Approved | Constitutions | N/A |

## ADR 021: Liquidity Pipeline Architecture (Wave 2B.2)
**Date:** 2026-07-08
**Context:** Liquidity analysis is inherently derived from structural price action, not from raw tick data or arbitrary candles. Building liquidity detectors directly off OHLC data risks duplicating structural logic and embedding subjective methodology into the core.
**Decision:** 
1. Liquidity rules must consume the **Structure Graph** and **Swing Events** to generate persistent **Liquidity Pool States** (e.g., `BuySideLiquidityPoolState`, `SellSideLiquidityPoolState`).
2. Interaction with liquidity must be modeled sequentially: `State -> Event -> Lifecycle`. 
3. The platform will never detect subjective methodology terms like "Stop Hunt". It will only emit objective geometric interactions (`LiquiditySweepEvent`, `LiquidityRaidEvent`, `LiquidityGrabEvent`), which methodology plugins can later interpret.
**Consequences:** Ensures the core framework remains strictly geometric, forcing liquidity definitions to remain purely structural and scalable across ICT, SMC, and Wyckoff methodologies.
