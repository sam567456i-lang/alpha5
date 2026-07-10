---
Authority: Level 1
Parent: Docs/Governance/Constitution.md
Children: None
Supersedes: dependency_map.md
Version: 1.0.0
Status: ACTIVE
---

# Program Dependency Map

This map explicitly defines the dependencies of the Auxiliary Programs (A-K) upon the deterministic trading core (Platforms 10-15), preventing hidden coupling and circular dependencies.

## Dependency Matrix

| Program | Depends On (Direct Consumer Of) | Forbidden From Accessing |
|---------|---------------------------------|--------------------------|
| **Program B: Knowledge Platform** | P10, P11, Data Platform, Operations | P12, P13 |
| **Program C: Research Platform** | P10, P11, P14, Knowledge Platform | P13 (Execution) |
| **Program D: AI Platform** | P10-P15 SDKs, Knowledge Platform | Internal Databases |
| **Program E: External Repository**| Foundation Layer, Data Platform | Live Execution (P13) |
| **Program F: Data Platform** | Foundation Layer | P10-P15 (Data is upstream) |
| **Program G: Operations** | All Platforms (Telemetry only) | Business Logic SDKs |
| **Program H: Infrastructure** | Foundation Layer | All Business Logic |
| **Program I: UI Platform** | P15 (Exclusively) | P10-P14 (Bypass is illegal) |

## Coupling Invariants
1. **The Isolation Rule:** Supporting programs may observe or consume deterministic outputs (via SDKs), but they may **never** write to deterministic databases or graphs.
2. **The Bypass Rule:** User Interfaces (Program I) may only ever consume Platform 15. They cannot reach directly into Platform 11 for an interpretation.
3. **The Execution Rule:** No program outside of Platform 13 and the Broker Adapter may generate live market orders. Research and AI platforms can generate *simulated* orders for P14 (Learning), but never real execution paths.
