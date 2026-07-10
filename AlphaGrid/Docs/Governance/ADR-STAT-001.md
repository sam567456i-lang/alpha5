---
Authority: Level 1
Parent: Docs/Governance/Constitution.md
Type: Architectural Decision Record
Title: ADR-STAT-001 Statistics Family Governance
Status: ACTIVE
Date: 2026-07-09
---

# ADR-STAT-001: Statistics Family Governance

## 1. Context
AlphaGrid is migrating to a deterministic 31-family capability architecture. The Statistics Family is the foundational layer upon which nearly all downstream capabilities (Trend, Volatility, Liquidity) depend. We must permanently define its scope and extension policies to prevent architectural drift.

## 2. Decision
We establish the Statistics Family under the strict 19-step Platform 10 Development Standard.

### 2.1 Authorized Engines
The family is limited strictly to the following engines:
- Distribution Engine
- Rolling Engine
- Normalization Engine
- Volatility Engine
- Confidence Engine
- Drift Engine
- Quality Engine

### 2.2 Extension Policy
Once frozen, the family must adhere to the following extension constraints:

**Allowed (Requires minor version bump):**
- Adding new objective mathematical measurements (e.g., adding a new standard deviation algorithm).
- Performance optimizations (O(n) improvements).
- Bug fixes.
- Documentation updates.

**Requires New ADR (Requires major version bump):**
- Modifying existing Evidence schemas (`DistributionEvidence`, etc.).
- Removing an engine or modifying its public contract.
- Changing upstream dependencies.
- Modifying the semantic meaning of an output.

**Strictly Forbidden:**
- Introducing methodology-specific logic (e.g., "ATR is expanding, so Trend is strong").
- Decision support or trading rules.

## 3. Consequences
- **Positive:** Guarantees that Statistics remains an objective, mathematically pure dependency for Platform 10. Prevents circular dependencies.
- **Negative:** Methodologies that require highly customized proprietary statistics must rebuild them in Platform 11, slightly increasing computation duplication in exchange for architectural purity.
