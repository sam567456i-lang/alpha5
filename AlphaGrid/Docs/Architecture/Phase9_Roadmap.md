# Phase 9: Declarative Strategy Framework Roadmap

With the Repository Architecture Freeze complete, Phase 9 focuses entirely on transitioning toward advanced trading logic.

## Phase 9 Sequence

1. **9A: Concept Completion**: Finalize foundational market concepts (e.g., Volatility Expansion, Momentum Confirmation) that rely on Indicator Engines.
2. **9B: Methodology Completion**: Formalize how concepts combine (e.g., Trend Following, Mean Reversion).
3. **9C: Signal Framework**: Define the boolean and discrete signaling emission protocols based on methodologies.
4. **9D: Declarative Strategies**: Develop strategies not by directly instantiating engines, but by declaring semantic dependencies.
5. **9E: Portfolio Coordination**: Execute multi-asset risk management and trade lifecycle tracking across declarative strategies.
6. **9F: Repository Validation & Freeze**: Perform a comprehensive structural audit of the new layer, culminating in the Phase 9 architecture lock.

## Declarative Strategy Design Constraint

**Rule**: Strategies must never instantiate indicators directly.

**❌ Invalid (Direct Coupling):**
```yaml
strategy:
  id: "trend_follower"
  indicator: "MACD"
```

**✅ Valid (Semantic Composition):**
```yaml
strategy:
  id: "trend_follower"
  requires:
    concepts:
      - "momentum_confirmation"
      - "volatility_expansion"
    methodologies:
      - "trend_following"
    signals:
      - "long_entry"
```

The runtime resolves the underlying indicator dependencies exclusively through the Master Capability Registry, allowing mathematical primitives to evolve without rewriting strategy files.
