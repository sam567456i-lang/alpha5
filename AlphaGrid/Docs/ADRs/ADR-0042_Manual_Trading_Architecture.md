# ADR-0042: Manual Trading Architecture

**Status:** Accepted
**Date:** 2026-07-05
**Context:** AlphaGrid's primary workflow must be permanently defined to prevent future automation dependencies from contaminating the core intelligence pipeline.

## Decision
AlphaGrid is permanently designated as an Institutional Trading Decision Support System (DSS) for manual discretionary traders.

## Consequences
- **Platform 14 (Recommendations)**: Output is a recommended trade plan, not an executable broker order.
- **Platform 15 (Risk)**: Evaluates the safety of the recommendation. Does not authorize execution.
- **Platform 16 (Portfolio)**: Provides portfolio intelligence (exposure, correlation). Does not perform automated portfolio rebalancing.
- **Platform 17 (Execution Guidance)**: Optimizes execution quality (timing, slippage estimation, partial entry planning, scaling guidance). Does not submit orders, connect to brokers, or click buy.

No automated execution logic, broker SDKs, or trade routing APIs may exist inside the production architecture. 

## Optional Future Expansion
Core AlphaGrid is Manual Trading. Optional Automation Modules may exist in the future.
If constructed, those modules must:
- Live entirely outside the production intelligence pipeline.
- Consume explicitly approved recommendations.
- Require completely separate governance and certification.
- Never modify upstream platforms.
