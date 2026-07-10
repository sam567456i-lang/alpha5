# ADR-003: Platform 11 Outputs Interpretations

## Status
Accepted - Frozen (Platform 11 Constitution)

## Context
If methodology code generates trading signals (e.g., "Buy 10 Lots"), the logic for methodology evaluation becomes tightly coupled with risk management, position sizing, and portfolio theory.

## Decision
Platform 11 is strictly barred from emitting actionable `Decision` or `TradingSignal` objects. It is only permitted to emit subjective `Interpretation` objects (e.g., `ContextInterpretation`, `BiasInterpretation`, `SetupInterpretation`). Platform 12 is solely responsible for determining if those interpretations are actionable.

## Consequences
- **Positive:** Total separation of methodology (reading the market) from decisioning (trading the market). Allows testing methodology accuracy independently of risk algorithms.
- **Negative:** Requires rigorous enforcement boundaries and SDK isolation to prevent developers from sneaking actionable logic into Platform 11.
