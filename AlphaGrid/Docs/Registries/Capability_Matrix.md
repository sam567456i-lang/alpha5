---
Authority: Level 1
Parent: Docs/Governance/Constitution.md
Children: None
Supersedes: coverage_matrix.md
Version: 1.0.0
Status: ACTIVE
---

# AlphaGrid Capability Matrix

This is the master inventory of all capabilities within the AlphaGrid ecosystem. It tracks ownership, input/output contracts, and certification status.

| Capability | Purpose | Domain | Platform | Program | Owner | Producer | Consumers | Inputs | Outputs | SDK | Dependencies | Lifecycle | Status | Version | Certification | Performance | Replay | Explainable | Docs | Tests | ADR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Fair Value Gap** | Measure Price Imbalances | Market | P10 | Trading Core | `ImbalanceEngine` | P10 Engine | P11, P14 | OHLCV | `FVGEvidence` | `EvidenceSDK` | None | Frozen | Active | 1.0 | Yes | 1ms | Yes | Yes | Yes | 100% | N/A |
| **Liquidity Pools** | Measure Untested Price Levels | Market | P10 | Trading Core | `LiquidityEngine` | P10 Engine | P11, P14 | OHLCV | `PoolEvidence` | `EvidenceSDK` | None | Frozen | Active | 1.0 | Yes | 2ms | Yes | Yes | Yes | 100% | N/A |
| **Market Structure** | Map Swings and Shifts | Market | P10 | Trading Core | `StructureEngine` | P10 Engine | P11, P14 | OHLCV | `SwingEvidence` | `EvidenceSDK` | None | Frozen | Active | 1.0 | Yes | 2ms | Yes | Yes | Yes | 100% | N/A |
| **ICT Sequences** | Identify 2022 Mentorship Setups | Methodology | P11 | Trading Core | `ICTProfile` | `SequenceEvaluator` | P12, P15 | P10 Evidence | `ICTInterpretation` | `MethodologySDK` | P10 | Certified | Active | 1.0 | Yes | <5ms | Yes | Yes | Yes | 100% | N/A |
| **SMC Sequences** | Identify Smart Money Concepts | Methodology | P11 | Trading Core | `SMCProfile` | `SequenceEvaluator` | P12, P15 | P10 Evidence | `SMCInterpretation` | `MethodologySDK` | P10 | Certified | Active | 1.0 | Yes | <5ms | Yes | Yes | Yes | 100% | N/A |
| **Wyckoff Cycles** | Identify Accum/Dist Phases | Methodology | P11 | Trading Core | `WyckoffProfile` | `SequenceEvaluator` | P12, P15 | P10 Evidence | `WyckoffInterpretation` | `MethodologySDK` | P10 | Certified | Active | 1.0 | Yes | <5ms | Yes | Yes | Yes | 100% | N/A |
| **AMT Value Areas** | Evaluate Volume Acceptance | Methodology | P11 | Trading Core | `AMTProfile` | `AuctionEvaluator` | P12, P15 | P10 Evidence | `AMTInterpretation` | `MethodologySDK` | P10 | Certified | Active | 1.0 | Yes | <5ms | Yes | Yes | Yes | 100% | N/A |
| **Volume Profile** | Extract Tick Volume Data | Volume | P10 | Trading Core | `VolumeEngine` | P10 Engine | P11, P14 | L2 Data | `VolumeEvidence` | `EvidenceSDK` | None | Proposed | Pending | 0.0 | No | N/A | Yes | Yes | No | 0% | N/A |
| **Order Flow** | Extract Delta and Imbalances | Volume | P10 | Trading Core | `OrderFlowEngine`| P10 Engine | P11, P14 | L2 Data | `OrderFlowEvidence` | `EvidenceSDK` | None | Proposed | Pending | 0.0 | No | N/A | Yes | Yes | No | 0% | N/A |
| **Feature Extraction** | Convert Graphs to Tensors | Decision | P12 | Trading Core | `FeatureExtractor` | P12 Engine | P12 | P11 Interpret | `DecisionVector` | Internal | P11 | Designed | In Progress | 0.1 | No | N/A | Yes | Yes | Yes | 50% | N/A |

*Note: This matrix will expand to thousands of rows as the project evolves.*
