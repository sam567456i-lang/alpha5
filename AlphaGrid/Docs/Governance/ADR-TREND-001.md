---
Authority: Level 1
Parent: Docs/Governance/Constitution.md
Type: Architectural Decision Record
Title: ADR-TREND-001 Trend Family Governance
Status: ACTIVE
Date: 2026-07-09
---

# ADR-TREND-001: Trend Family Governance

## 1. Context
The Trend Family follows the Statistics Family in the dependency graph. Its role is to translate mathematical statistics into objective descriptors of directional momentum. We must enforce strict boundaries so Trend does not accidentally implement Swing logic or Methodology labels.

## 2. Decision
The Trend Family will strictly adhere to the 19-step Platform 10 Development Standard. 

### 2.1 Authorized Engines
The family is limited strictly to:
- Direction Engine
- Strength Engine
- Geometry Engine
- State Engine
- Persistence Engine

### 2.2 Extension Policy
**Allowed (Requires minor version bump):**
- Adding new measurements of geometry or strength (e.g., adding `TrendConsistencyEvidence`).
- Performance optimizations.

**Requires New ADR (Requires major version bump):**
- Removing an engine.
- Changing semantic structure of outputs.

**Strictly Forbidden:**
- Implementing swing generation logic (e.g., Higher High, Lower Low detection).
- Emitting methodology-specific subjective labels (e.g., "Bullish Order Block Context", "Wyckoff Markup").
- Coupling directly to an engine instead of consuming Evidence via the Event Bus.

## 3. Consequences
- **Positive:** Downstream methodologies (ICT, SMC, AMT) can all reuse the same Trend calculations without coupling to conflicting terminologies.
- **Negative:** Trend may feel "incomplete" to a purely subjective trader until mapped through Platform 11.
