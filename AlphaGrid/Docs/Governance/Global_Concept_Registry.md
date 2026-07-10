---
Authority: Level 1
Parent: Docs/Governance/Constitution.md
Type: Concept Registry
Status: ACTIVE
Version: 1.0.0
---

# Global Concept Registry

This registry tracks the single ownership of every analytical concept within the Platform 10 ecosystem, as mandated by Constitution Rule 7. A concept may only have ONE owner.

| Concept | Owner Family | Producer Engine | Consumers | Lifecycle | DTO | SDK | Certification |
|---|---|---|---|---|---|---|---|
| **Swing High/Low** | Swing | PersistenceEngine | Range, Geometry, Liquidity Objects | Immutable | `SwingEvidence` | Core | Frozen |
| **EQH / EQL** | Swing | PivotEngine | Liquidity Objects | Immutable | `PivotEvidence` | Core | Frozen |
| **Range High/Low** | Range | BoundaryEngine | Geometry, Liquidity Objects | Immutable | `RangeBoundaryEvidence` | Core | Frozen |
| **Intersection** | Geometry | IntersectionEngine | Liquidity Events, Structure Events | Immutable | `IntersectionEvidence` | Core | Frozen |
| **Distance** | Geometry | DistanceEngine | Liquidity Objects, P11 | Immutable | `DistanceEvidence` | Core | Frozen |
| **PDH / PDL** | Liquidity Objects | ReferenceLevelEngine | Liquidity Events | Stateful | `LiquidityObjectEvidence` | Core | Planned |
| **Sweep** | Liquidity Events | SweepEngine | P11 (ICT/SMC) | Event | `SweepEventEvidence` | Core | Planned |
| **BOS / CHOCH** | Structure Events | BreakEngine | P11 (ICT/SMC) | Event | `BreakEventEvidence` | Core | Planned |
| **FVG / Gap** | Imbalance Objects | ImbalanceEngine | Imbalance Events | Stateful | `ImbalanceObjectEvidence` | Core | Planned |
| **Filled FVG** | Imbalance Events | FillEngine | P11 (ICT/SMC) | Event | `FillEventEvidence` | Core | Planned |
| **Order Block** | Institutional Zones | ZoneEngine | P11 (ICT/SMC) | Stateful | `ZoneEvidence` | Core | Planned |

*(Note: This registry will continually expand as remaining families are implemented through their respective 19-step execution pipelines.)*
