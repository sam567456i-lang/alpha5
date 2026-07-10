---
Authority: Level 1
Parent: Docs/Governance/Constitution.md
Children: None
Supersedes: None
Version: 1.0.0
Status: ACTIVE
---

# Roadmap Freeze Policy

This policy clarifies the distinction between freezing an Architecture and freezing a Product. 

Contributors must understand that declaring a Platform "Frozen" does not mean development stops; it means the *framework* governing that development is locked.

## The 4 States of AlphaGrid

1. **Architecture: FROZEN**
   - *Definition:* The structural paradigms (e.g., P10 emits Evidence, P11 consumes Evidence via Evaluators).
   - *Implication:* Modifying these paradigms is illegal without an extensive ADR process and massive regression testing.

2. **Platform: FROZEN (Selective)**
   - *Definition:* The core processing loop and the SDK interface of a specific platform (e.g., `SequenceEvaluator`).
   - *Implication:* The core engine cannot be touched. However, the Platform can accept new modular plugins (e.g., a new YAML profile).

3. **Capability/Implementation: GROWING**
   - *Definition:* The actual features (e.g., Order Flow Engine, new TradingView external adapter).
   - *Implication:* This is where 95% of future engineering effort will occur. Implementations continuously expand within the boundaries of the frozen architecture.

4. **Product: CONTINUOUS**
   - *Definition:* The user experience, AI interaction patterns, UI dashboards.
   - *Implication:* Highly malleable. Product design iterates constantly (e.g., changing how a Decision Vector is rendered in the UI), but because it consumes frozen SDKs, it can never break the core trading determinism.
