# Platform 10: Methodology Composition Engine Boundary Contract

## Statement of Purpose
Platform 10 is the analytical aggregator of AlphaGrid. It is mathematically and architecturally prohibited from generating actionable trading signals. Its sole purpose is to consume discrete semantic concepts and produce higher-level methodology assessments and statistical consensus maps.

## Ingestion Contract
Platform 10 **MUST ONLY** consume:
1. `ConceptDTO` (from Platform 9)
2. `MethodologyContextDTO` (The unified, immutable runtime envelope)
3. YAML Registry Configuration (via `RegistryResolver`)

## Production Contract
Platform 10 **MUST ONLY** produce:
1. `MethodologyDTO` (The individual plugin's analytical output)
2. `MethodologyConsensusDTO` (The aggregated probability matrix across all active methodologies)

## Prohibited Outputs
Under no circumstances may Platform 10, or any of its executing plugins, produce or modify:
- Liquidity Maps
- Structural Nodes
- Spatial Zones
- Raw Semantic Concepts
- Strategy Signals
- Trade Executions
- Portfolio Decisions
- Order Routing Directives

> [!CAUTION]
> Violation of this boundary contract breaks the acyclic dependency graph of AlphaGrid and introduces execution risks. This boundary MUST be enforced by the `MethodologyCertificationSuite` during CI/CD.

## Plugin Sandbox Contract
Methodology plugins operate in a strict sandbox environment. Plugins **MUST NOT** directly access:
- The filesystem (no reading/writing configurations or data)
- The network (no API calls)
- The database
- The cache
- The event bus
- Any other plugin instance

Plugins receive all required configuration and data through the `MethodologyContextDTO`. If a plugin attempts external I/O, it is non-deterministic and fails certification.

## Analytical Rule Execution Constraint
Analytical Rules may evaluate evidence only. They must never create, modify, or invalidate domain entities (`LiquidityDTO`, `StructureDTO`, `ZoneDTO`, `ConceptDTO`, or `MethodologyDTO`). They produce only immutable `RuleEvidenceDTO` objects.

## Rule Composition and Orchestration Constraint
A rule may consume only certified evidence produced by lower-tier rules. A rule must never invoke another rule directly. The `RuleExecutionPlanner` is the only component permitted to schedule rule execution. Rules, runtimes, and methodologies may never invoke another rule directly.

## Detector Boundary Caution
Do not allow analytical rules to slowly become miniature detectors. A rule should never:
- Search raw candles
- Detect swings
- Calculate pivots
- Create zones
- Create concepts

Every rule must assume that Platform 8 and Platform 9 have already produced certified domain objects. The rule layer should only interpret those outputs and produce evidence.
