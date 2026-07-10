---
Authority: Level 1
Parent: Docs/Governance/Constitution.md
Type: Architectural Decision Record
Title: ADR-RANGE-001 Range Family Governance
Status: ACTIVE
Date: 2026-07-09
---

# ADR-RANGE-001: Range Family Governance

## 1. Context
The Range family manages spatial zones. If Range logic duplicates Swing logic (e.g. independently detecting HH/LL to form a range), we violate Platform 10's Single Source of Truth (Rule 4). If Range begins inferring "liquidity sweeps" or "accumulation phases", we violate Rule 5 (No Semantic Inflation).

## 2. Decision
The Range Family will act strictly as a consumer of `SwingEvidence` and `TimeEvidence`, producing bounded geometry without subjective classification.

### 2.1 Pure Consumer Rule
The Range Family will **never** contain a pivot detection algorithm. It must subscribe to the `PivotLifecycleEvidence` or `SwingRelationshipEvidence` emitted by the Swing Family.

### 2.2 Strict Domain Boundary
The Range Family produces boundaries (High, Low, Midpoint) and scalar state (Expansion, Compression). It **shall not** produce Liquidity Pools or Market Structure Shifts.

### 2.3 Time-Based Ranges
The Temporal Engine may produce ranges bounded exclusively by time (e.g. 09:30 - 10:00). These are distinct from structural ranges but output the same `RangeBoundaryEvidence` for uniform downstream consumption.

## 3. Consequences
- **Positive:** Downstream consumers (e.g., Geometry for Channels, Liquidity for EQH pools) have a single, unified interface for all range-based data, regardless of whether the range was structural or temporal.
- **Negative:** Range is heavily dependent on the Swing family's accuracy for structural boundaries.
