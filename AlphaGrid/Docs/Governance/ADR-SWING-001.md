---
Authority: Level 1
Parent: Docs/Governance/Constitution.md
Type: Architectural Decision Record
Title: ADR-SWING-001 Swing Family Governance
Status: ACTIVE
Date: 2026-07-09
---

# ADR-SWING-001: Swing Family Governance

## 1. Context
Pivots and Swings form the foundational geometry for all downstream market structure and liquidity analysis. If the Swing Family leaks subjective terminology or locks into a single hardcoded algorithm, it forces downstream methodologies to rebuild their own pivot extractors, creating dependency chaos.

## 2. Decision
The Swing Family will strictly implement objective pivot logic and enforce a recursive swing lifecycle. 

### 2.1 Pluggable Pivots
The Pivot Engine MUST not hardcode a single algorithm. It must define a `PivotDetectionPolicy` interface, allowing `N-Bar Fractal`, `ATR Adaptive`, or `ZigZag` algorithms to be configured externally.

### 2.2 Lifecycle Enforcement
Downstream consumers must explicitly request the lifecycle state of a pivot. Candidate or Developing pivots must never be passed to Structure engines without the consumer expressly opting in to unconfirmed data.

### 2.3 Strict Domain Boundary (No Semantic Inflation)
The Swing Family **shall not** identify Break of Structure (BOS), Change of Character (CHoCH), or Liquidity Sweeps. It produces `SwingEvidence` (e.g. Higher High), which the Market Structure family consumes to determine BOS.

## 3. Consequences
- **Positive:** A single, highly optimized pivot engine powers everything. No duplicated N-bar loops anywhere else in the system.
- **Negative:** Increased complexity in the Pivot Engine due to pluggability and the multi-state lifecycle management.
