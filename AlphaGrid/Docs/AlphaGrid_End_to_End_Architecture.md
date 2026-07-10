---
Authority: Level 1
Parent: Docs/Governance/Constitution.md
Children: None
Supersedes: None
Version: 1.0.0
Status: ACTIVE
---

# AlphaGrid End-to-End Architecture

This document defines *how* AlphaGrid works, detailing the four foundational layers, the deterministic internal pipeline, the consumer flow, and the supporting programs.

## 4-Layer Hierarchy

1. **Layer 1 — Foundation (Phase 0):** Nothing trading-specific. Contains configurations, logging, DI, caching, and CI/CD.
2. **Layer 2 — Data Platform:** Converts APIs into the Canonical Market Dataset.
3. **Layer 3 — Market Intelligence Pipeline:** The deterministic core (Platforms 10-15).
4. **Layer 4 — Supporting Platforms & Applications:** Auxiliary non-deterministic systems (Knowledge, AI, UI).

## Complete Producer -> Consumer Chain
```
Foundation
        │
        ▼
Data Platform
        │
        ▼
Platform 10 (Objective Evidence)
        │
        ▼
Platform 11 (Methodology Interpretation)
        │
        ▼
Platform 12 (Decision Support)
        │
        ▼
Platform 13 (Execution Intelligence)
        │
        ▼
Platform 14 (Learning & Analytics)
        │
        ▼
Platform 15 (User Interfaces & APIs)
```

## Internal Flow (Life of a Candle)
1. **Exchange** -> Market Feed
2. **Normalizer** -> Data Lake
3. **Geometry/Indicators (P10)** -> Evidence Graph
4. **Evaluators (P11)** -> Interpretation Graph
5. **Decision Engine (P12)** -> Decision Candidates & Execution Plan
6. **Execution Planner (P13)** -> Order Sequence
7. **Broker Adapter** -> Trade Result
8. **Learning Engine (P14)** -> Statistics

## User Flow (Consumer Example)
1. **Dashboard (P15)** requests BTCUSDT context.
2. **P15 queries P11 SDK:** P11 returns Narrative Projection (e.g., Bullish Context, Liquidity Draw).
3. **P15 queries P12 SDK:** P12 returns Decision Candidates (e.g., LONG, 82% Confidence).
4. **P15 queries P13 SDK:** P13 returns Execution Plan (Entry Zone, Scale In).
5. User presses "Execute".
6. **P13** routes to Broker Adapter. Trade finishes, flows into **P14** for learning and attribution.
