---
Document ID: CONST-001
Title: "Target Operating Architecture"
Version: 3.0.0
Governance Version: 1.0.0
Architecture Version: 1.0.0
Phase: 10
Owner: ArchitectureTeam
Category: Constitutions
Maturity: "Level 5: Institutionally Frozen"
Implementation Status: Validated
Current Phase: 10
Future Phase: N/A
Last Validated Phase: 10
Review Date: 2026-07-03
Dependencies: []
Referenced By: []
---

# AlphaGrid Infinity X — Target Operating Architecture (v3.0 Institutional)

> [!IMPORTANT]
> This document is the absolute source of truth for AlphaGrid's architectural design. It defines the structural boundaries, contracts, and core engine rules. Engineering practices, testing, operational monitoring, and recovery protocols are governed by their respective standard documents.

---

## 1. Architectural Core Principles

### 1.1 Architectural Dependency Rule
Every Program must explicitly declare its boundaries to prevent architectural shortcuts.
- **Consumes**: Required upstream inputs.
- **Produces**: Outputs generated.
- **Allowed Downstream**: Permitted consumers of the output.
- **Forbidden Downstream**: Layers that must NEVER directly consume this output.
*(Example: Price Geometry Consumes: Market Intelligence | Produces: Geometry Objects | Allowed Consumer: Feature Infrastructure | Forbidden Consumers: Strategy, Portfolio, Evidence).*

### 5. Multi-Methodology Structural Intelligence Platform
The platform strictly enforces the abstraction between objective market geometry and subjective market interpretation.

1. **Geometry Engine Orchestrator**: Executes stateless `AbstractGeometryEngine`s in a topologically sorted DAG.
2. **Immutable Geometry Objects**: Geometry objects (e.g., OrderBlocks) are immutable. State transitions emit new versioned objects (e.g., `BROKEN`, `MITIGATED`).
3. **Methodology Agnostic**: The `MarketStructureConceptGenerator` emits `MARKET_STRUCTURE_EVENT` primitive signals that are fundamentally objective (BOS, CHOCH, Liquidity Sweeps).
4. **Methodology Engines**: Methodologies (`SMCMethodology`, `WyckoffMethodology`) independently consume objective primitive signals to emit subjective decisions based on their rule sets.

### 6. Zero-Tolerance Simulation Rule (Contract Ownership)
Every responsibility, contract, and domain must have **exactly one** authoritative owner. Never allow duplicate implementations.
- Feature Registry → Feature Domain
- Expected Bars → Session Engine
- Evidence Score → Evidence Engine

### 1.3 Universal Engine Contract
Every engine across the entire platform MUST implement an identical architectural contract. The metadata must expose:
`Engine ID, Version, Owner, Registry, Consumes, Produces, Dependencies, Configuration schema, Lifecycle state, Fingerprint, Quality metadata`.
This enables automatic pipeline inspection and routing.

### 1.4 Canonical Object Rule
Every canonical object flowing through the pipeline must expose consistent baseline metadata:
`ID, Version, Owner, Timestamp, Fingerprint, Confidence, Quality, Lineage, Lifecycle`.

### 1.5 Research Object Lineage
Every research object carries immutable lineage, allowing complete traceability from a trade recommendation back to originating market data.
`Raw Data → Normalized Data → Geometry → Feature → Concept → Primitive Signal → Methodology → Strategy → Validation → Evidence → Decision`

### 1.6 Canonical Consume Rule
A stage is NOT complete merely because it produced output. A stage is ONLY considered complete when its output is successfully consumed by the immediate downstream stage during a canonical execution.

### 1.7 Family Freeze Rule
A family is frozen **only** when all of the following conditions are met:
1. Every planned strategy in that family is implemented.
2. All shared components (features, geometry, concepts, methodologies) required by the family are complete.
3. Family regression testing passes.
4. Documentation is synchronized.
5. The Master Project Ledger is updated.
6. The Master Capability Registry is updated.

Individual strategies being complete does NOT freeze a family.

### 1.8 Shared Component Freeze Rule
Shared platform components (Features, Concepts, Methodologies) must never freeze simply because one Strategy Family finished implementing them. They advance through:
`Candidate -> Implemented -> Validated -> Reusable -> Multi-family Validated -> Frozen`
Example: A `TrendConcept` is not frozen because EMA works. It freezes only after Trend, Momentum, Breakout, and Mean Reversion families have reused it successfully.

### 1.9 Validation Distinctions
The lifecycle explicitly distinguishes between two validation scopes:
- **Technical Validation**: Verifies determinism, memory budget, runtime budget, registry compliance, DTO schema compliance, and dependency resolution.
- **Quantitative Validation**: Verifies expectancy, Sharpe ratio, CAGR, maximum drawdown, win rate, and stability across regimes.

### 1.10 Dependency Validation Rules
Dependencies defined in the Master Capability Registry (`depends_on`) are enforced at runtime via the Dependency Registry:
- **Circular Dependencies**: Fail validation immediately.
- **Missing Dependencies**: Fail validation immediately.
- **Version Incompatibilities**: Fail validation if the required DTO schema or component version is incompatible.
- **Disabled Dependencies**: If a required upstream component is disabled via the Feature Switch Manager, the dependent component cannot activate and fails validation.

### 1.11 Repository Quality Gates
- **CI Merge Gates**: Pull requests require clean unit, integration, and deterministic output tests.
- **Repository Health Check**: Enforced prior to cross-family regression. Strictly validates: duplicate registrations, orphan capabilities, unused switches, circular dependencies, DTO schema compatibility, configuration compatibility, capability version compatibility, dependency version compatibility, registry checksum validation, and switch inheritance validation.
- **Incremental Regression**: Runs the Current Family + All previously Frozen Families. This is fast and runs every family.
- **Full Repository Regression**: The ultimate release gate. Runs EVERYTHING (every capability, every switch, every registry, every pipeline, every DTO).
- **Component Freeze**: Shared components require Multi-family Validation before freezing.
- **Family Freeze**: Strategies do not freeze until Research Validation and Architecture Review.
- **Architecture Review**: Mandatory manual gate prior to freezing major capabilities.

### 1.12 Pipeline Contract Rules
The canonical runtime flow ensures strict separation of concerns. Every phase must adhere to the following contract:
- **Accepts Only Defined DTOs**: A phase can only consume the specific DTOs defined in the Master Interface Specification.
- **Returns Only Defined DTOs**: A phase can only output its canonical DTO.
- **No Bypassing**: Phases must never bypass intermediate layers (e.g., a Strategy cannot consume Raw Data; it must consume Concepts/Methodologies).
- **Determinism**: Given identical inputs, configuration, and version, a phase must produce exactly the same output.

### 1.13 Feature Switch Inheritance Rules
The Feature Switch Manager controls domains (Infrastructure, Data, Features, Families), not individual indicators.
- **Lifecycle States**: `Registered -> Installed -> Available -> Enabled -> Paused -> Disabled -> Retired -> Deprecated -> Removed`.
- **Legal Transitions**: States advance or retreat only to adjacent states. Skipping states is prohibited (e.g., `Registered` cannot jump to `Enabled`).
- **Parent Disablement**: Disabling a parent domain disables all its child capabilities.
- **Child Override**: Child capabilities cannot override a disabled parent.
- **Shared Components**: Shared components remain registered and operational even if a specific Strategy Family is disabled, provided another active component consumes them.

### 1.14 Universal Query Engine
The Universal Query Engine provides platform-wide capabilities for querying objects. It is responsible for:
`Search, Filter, Sort, Group, Rank, Aggregate, Export`.

### 1.15 Canonical Freeze Lifecycle
Nothing can freeze unless it traverses the complete governance path:
`Architecture Approved -> Implemented -> Unit Validated -> Integration Validated -> Technical Validation -> Repository Validation -> Cross-Family Validation -> Research Validation -> Architecture Review -> Production Review -> Freeze Vote -> Frozen`

### 1.16 Knowledge Graph Relationships
The Dependency Registry supports the following relationship types:
`uses, depends_on, derived_from, validated_by, supports, contradicts, supersedes, invalidates, extends, duplicates, replaced_by, improves, consumes, produces`

### 1.17 Validation Engine
A dedicated platform-wide infrastructure service responsible for:
- DTO validation, Schema validation, Registry validation, Configuration validation
- Dependency Graph validation, Version Compatibility, Runtime Constraints
- Memory Budget, Performance Budget, Determinism verification

### 1.18 Registry Manager
Single authority for registry loading, validation, versioning, dependency checking, and lifecycle management across all registries. All registries implement the `RegistryInterface`: `load(), save(), validate(), search(), dependency_lookup(), version_lookup(), lifecycle(), serialize(), deserialize(), migrate(), snapshot(), rollback()`.

### 1.19 RuntimeContext
Every engine receives an **immutable** `RuntimeContextDTO` alongside its `PipelineObject` input. It is constructed once at pipeline start and never mutated during execution. Mutable state belongs exclusively in the State Manager.
Contents: Execution ID, Market, Exchange, Asset, Timeframe, Session, Timezone, Configuration Snapshot (with effective configuration checksum), Version Snapshot, Registry Snapshot, Scheduler State, Enabled Switches, Execution Mode (Backtest / Paper / Live), Pipeline Start Time.

### 1.20 Configuration Hierarchy
Configuration is resolved through a deterministic override chain:
`Global -> Environment -> Market -> Exchange -> Asset -> Strategy -> Experiment -> Runtime Override`
Rules:
- Every override records its source.
- Effective configuration is computed once at pipeline start.
- Effective configuration checksum is stored in RuntimeContext.
- Lower levels override higher levels.

### 1.21 Pipeline Version Snapshot
A `PipelineSnapshotDTO` is mandatory for every pipeline execution and research experiment. Contents: DTO versions, Feature versions, Geometry versions, Concept versions, Methodology versions, Signal versions, Strategy versions, Registry versions, Configuration version, Git commit, Dependency lock, Python version, Package versions.

### 1.22 Event Bus
The runtime transitions from synchronous chaining to event-driven orchestration: `Scheduler -> Event Bus -> Pipeline`.
**System Events**: Startup, Shutdown, HealthFailure.
**Market Events**: NewTick, NewBar, SessionOpen, SessionClose, EconomicEvent.
**Trading Events**: SignalGenerated, DecisionApproved, OrderFilled, PositionClosed, RiskAlert.

### 1.23 State Manager
Centralized service owning all mutable runtime state. No engine may persist state internally beyond temporary computation.
Owns: Positions, Orders, Portfolio, Warmup Buffers, Rolling Windows, Strategy State, Session State, Runtime Cache.

### 1.24 Cache Hierarchy
Unified cache architecture managed through the State Manager. Each cache specifies: Owner, Key, TTL, Eviction Policy, Invalidation Trigger, Persistence.
Layers: Feature Cache, Geometry Cache, Concept Cache, Strategy Cache, Research Cache.

### 1.25 Error Taxonomy
All engines return typed results, separating outcomes from errors.
**Execution Results**: Success, Warning.
**Error Types**: Configuration, Validation, Dependency, Retryable, Timeout, Cancelled, Fatal.

### 1.26 Health Model
Runtime health is monitored at three levels:
**Component Health**: Healthy, Degraded, Offline.
**Pipeline Health**: Running, Waiting, Recovering, Failed.
**Platform Health**: Healthy, Warning, Critical.

### 1.27 Plugin Lifecycle
Plugins traverse a strict state machine enforced by the Plugin Manager:
`Discovered -> Verified -> Installed -> Loaded -> Registered -> Initialized -> Running -> Paused -> Stopped -> Unloaded`

### 1.28 Dependency Lifecycle
Dependencies traverse a strict state machine enforced by the Dependency Registry:
`Missing -> Resolved -> Loaded -> Verified -> Compatible -> Active -> Deprecated`
Incompatibility transitions explicitly to `Incompatible` and fails validation rather than silently degrading.

### 1.29 Market Abstraction
Exchange-specific and broker-specific code is encapsulated behind a layered adapter hierarchy:
`MarketAdapter -> ExchangeAdapter -> BrokerAdapter -> ExecutionGateway`
The ExecutionGateway isolates broker APIs from execution logic.

### 1.30 AI Boundary
AI (Phase 12) must never receive arbitrary pipeline objects directly. The boundary is enforced through three frozen DTOs:
`AIInputDTO : PipelineObject` — curated inputs to the AI subsystem.
`AIOutputDTO : PipelineObject` — structured AI predictions/evaluations.
`AIEvidenceDTO : PipelineObject` — explainability artifacts.

### 1.31 Policy Engine
A dedicated platform-wide infrastructure service that enforces all platform rules. Subsystems query the Policy Engine rather than implementing policy checks independently.
Responsibilities: Feature Switch Policies, Risk Policies, Configuration Policies, Version Compatibility Policies, Merge Policies, Runtime Policies, Security Policies.

### 1.32 Health Audit Definitions
The Repository Health Audit uses the following strict definitions to detect architectural decay and enforce compliance:
- **Duplicates**: Multiple implementations sharing the same component ID, identical checksums, or registering the same feature switch.
- **Orphans**: Valid orphans are foundational components (e.g., Features/Concepts) actively maintained but not yet wired to a strategy. Invalid orphans are dead code, unreachable classes, or deprecated logic with no planned consumers.
- **Dependency Violations**: Any import or architectural coupling that violates the downward-flow rule (e.g., Features importing Concepts) or creates a circular dependency.
- **Unreachable Capability**: A capability registered in the Capability Registry but mathematically impossible to trigger via the canonical pipeline.
- **Dead Switch**: A feature switch that exists in configuration but is never evaluated by the Policy Engine or any active component.
- **Dead Registry Entry**: A component registered in `master_capability_registry.yaml` that has been deleted or renamed in the source code.
- **Unused DTO**: A Data Transfer Object defined in the schemas that is never instantiated or consumed by any active pipeline layer.
- **Unused Configuration**: Configuration keys that exist in the config files but are never read by the application.
- **Unused Plugin**: A plugin that is discovered but never loaded or executed by the Plugin Manager.
- **Broken Migration**: A migration where the source and destination SHA-256 hashes do not match, or import paths were not fully updated.
- **Drift**: Any divergence between the `architecture_bible.md`, the `master_capability_registry.yaml`, and the actual running Python code (Version drift, Schema drift, or Configuration drift).

---

## 2. Target Operating Architecture

## Canonical Runtime Flow
The explicit execution dependency chain for AlphaGrid is strictly defined as:
`Market Data -> Market Intelligence -> Feature Store -> Geometry -> Concepts -> Methodologies -> Signals -> Strategies -> Strategy Intelligence -> Decision Engine -> Risk -> Portfolio -> Execution`

### Post-Strategy Decision Pipeline
`StrategyDTO -> DecisionCandidateDTO -> DecisionDTO -> RiskDecisionDTO -> ExecutionPlanDTO -> ExecutionDTO`

### Runtime Orchestration
`Market Event -> Event Bus -> Runtime Scheduler -> Pipeline Dispatcher -> Dependency Resolver -> Execution DAG -> Pipeline Executor (receives RuntimeContext + PipelineObject) -> Results -> Event Bus`

This flow is strictly enforced. No component may skip a layer or directly call a later phase. Communication between layers is strictly managed by defined Data Transfer Objects (see `master_interface_specification.md`).

========================================================================
                        FOUNDATION LAYER
========================================================================
Master Constitution
Architecture Rules
Repository Rules
Production Standards
Scientific Governance
Coding Standards
Testing Standards
Security Standards
Performance Standards

========================================================================
                      INFRASTRUCTURE LAYER
========================================================================
Configuration
Dependency Injection
Event Bus
Scheduler
Worker Pool
Logging
Metrics
Monitoring
Secrets
Caching
Message Queue
Storage
CLI
REST API
WebSocket API

========================================================================
                          DATA LAYER
========================================================================
Exchange APIs
Broker APIs
Historical Data
Live Market Data
Options Chain
News
Economic Calendar
Alternative Data
↓
Validation
↓
Cleaning
↓
Normalization
↓
Versioning
↓
Storage
↓
Data Quality Engine
↓
Market Database

========================================================================
                    MARKET INTELLIGENCE LAYER
========================================================================
                    MARKET INTELLIGENCE (Phase 4)
========================================================================

**Purpose**: Fetches and processes external, macro, intermarket, and breadth data from the outside world or aggregated indices.
**Boundary Rule**: Market Intelligence connects to outside data providers or heavy aggregators. It feeds data into the Feature Store.

Asset Metadata
Timezone Normalization
Currency Conversion
Macro Intelligence
Intermarket Intelligence
Institutional Ownership Intelligence
Economic Calendar Intelligence
Corporate Earnings
Dividend Calendar
IPO Calendar
Index Rebalancing
ETF Flows
Mutual Fund Flows
FII/DII Flows
Corporate Actions
Trading Halts
Circuit Breakers
Market Regime
Sector Rotation
OHLCV
Breadth
Regime Detection
Volatility
Liquidity

========================================================================
                       PRICE GEOMETRY
========================================================================
Geometry Confidence
Geometry Quality Score
Geometry Conflict Detection
Geometry Merge/Split Detection
Fractal Geometry
Nested Swing Trees
Wave Detection
Compression/Expansion
Volatility Geometry
Geometry Lineage

========================================================================
                       FEATURE STORE (Phase 5)
========================================================================

**Purpose**: Strictly mathematical, stateless components that compute atomic features.
**Boundary Rule**: The Feature Store must NEVER fetch data itself. It only computes math based on inputs provided by Phase 3 (Data Hub) or Phase 4 (Market Intelligence).

--- Feature DAG ---
Feature Registry
Feature Cache
Versioning
Warm-up Management
Offline Feature Store
Online Feature Store
--- Categories ---
Price Features
Volume Features
Order Flow Features
Volatility Features
Market Breadth
Market Internals
Options Features
--- Atomic Features ---
EMA, SMA, RSI, ATR, MACD, Bollinger, Donchian, ADX, VWAP, OBV, CMF, MFI, SuperTrend, Keltner, CCI, ROC, Momentum, Volatility, Volume
Relative Strength, Currency Strength, Seasonality, Ownership, Calendar-derived features
Future: Greeks, IV, Gamma, Delta, OI, Footprint

========================================================================
                     CONCEPT ENGINE
========================================================================
Concepts must remain strictly semantic and methodology-agnostic. No methodology-specific concepts (e.g., SMC Bullish Setup, Wyckoff Spring) belong in this tier.

Trend
Momentum
Liquidity
Structure
Volatility
Breakout
Continuation
Breadth Expansion
Relative Strength
Currency Strength
Participation
Strength
Weakness
Trend Exhaustion
Rotation
Market Pressure
Market Balance
Market Imbalance
Market Efficiency
Risk Appetite

========================================================================
                  METHODOLOGY ENGINE (Phase 8)
========================================================================

Price Methodologies:
- Trend
- Momentum
- Breakout
- Mean Reversion

Market Methodologies:
- Breadth
- Intermarket
- Relative Strength
- Currency
- Macro
- Seasonality

Market Structure:
- SMC
- Wyckoff
- Auction
- ICT

Statistical Methodologies:
- Factor

========================================================================
                      SIGNAL ENGINE
========================================================================
Methodology Evaluation
↓
Signal Generation
↓
Signal Ranking
↓
Confidence
↓
Signal Explanation
↓
Signal Registry

========================================================================
                     DECISION INTELLIGENCE
========================================================================
Rule Engine
Machine Learning
Deep Learning
Ensemble
Meta AI
Confidence Fusion
Strategy Voting
Strategy Ranking
Market Regime Selection
Decision Explainability

========================================================================
                     STRATEGY LIBRARY & CAPABILITIES
========================================================================
> [!NOTE]
> The Architecture Bible describes the design and boundaries of the system. It does **not** maintain a manual list of strategies or indicators.
> 
> The authoritative inventory of all Features, Geometry, Concepts, Methodologies, and Strategies is maintained strictly in the `Master Capability Registry` (`master_capability_registry.yaml`).
> 
> A read-only script (`Scripts/generate_documentation_from_registry.py`) automatically generates the following documents from the registry:
> - `Docs/ai_compatibility_matrix.md`
> - `Docs/capability_matrix.md`
> - `Docs/strategy_catalog.md`
> - `Docs/family_summary.md`
> - `Docs/documentation_index.md`

Every Strategy must follow the architectural flow:
`Features → Concepts → Methodology → Signal → Decision`

========================================================================
                  RESEARCH FRAMEWORK
========================================================================
Research Hypotheses
Experiments
Experiment Registry
Experiment Config
Version Locking
Backtest
Walk Forward
Monte Carlo
Statistical Validation
Promotion Rules
Research Registry
Candidate Registry
Scientific Reports
--- Data Science & ML ---
Dataset Registry
ML Dataset Generation
Training Pipelines

========================================================================
                  AI RESEARCH PLATFORM
========================================================================
Research Assistant
Repository Auditor
Architecture Reviewer
Experiment Planner
Feature Generator
Hypothesis Generator
Code Generator
Test Generator
Documentation Generator
Performance Reviewer
Continuous Learning

========================================================================
                 EXTERNAL AI INTEGRATION
========================================================================
HKUDS Vibe-Trading
OpenAI
Future Agent Frameworks
Research APIs
LLM Providers
Adapter Layer
Compatibility Layer
Repository Validator
Architecture Validator
Translation Layer

========================================================================
                 STRATEGY INTELLIGENCE (PHASE 13)
========================================================================
This engine handles the massive coordination of 150+ deterministic strategies.
The canonical pipeline is:
`Strategy -> Strategy Intelligence (optional) -> Risk -> Portfolio`

**Workflow:**
Market State
↓
150+ Strategies
↓
Rule-Based Evaluation
↓
AI Evaluation (Optional, when available)
↓
Performance Ranking
↓
Conflict Resolution
↓
Consensus Engine
↓
Final Strategy Consensus
↓
Risk Engine

========================================================================
                   PORTFOLIO ENGINE
========================================================================
Capital Allocation
Position Sizing
Risk Budget
Exposure (Factor, Sector, Currency, Country, Beta, Style)
Sector Allocation
Correlation Control
Portfolio Optimization
Diversification
Dynamic Rebalancing

========================================================================
                    RISK ENGINE
========================================================================
Trade Risk
Portfolio Risk
Max Drawdown
Daily Loss
Exposure Limits
Circuit Breakers
Kill Switch
Stress Testing
Scenario Analysis

========================================================================
                 EXECUTION INTELLIGENCE
========================================================================
Execution Planning
Smart Routing
TWAP
VWAP
Iceberg
Slippage Control
Latency Control
Partial Fill Management
Broker Selection
Retry Logic
Execution Monitoring
Execution Analytics (Transaction Cost Analysis, Fill Quality, Slippage Attribution, Market Impact, Latency, Queue Position)

========================================================================
                     LIVE RUNTIME
========================================================================
Paper Trading
↓
Shadow Trading
↓
Limited Live
↓
Production Live
↓
Performance Monitoring
↓
Health Monitoring
↓
Alerts
↓
Recovery

========================================================================
                   KNOWLEDGE SYSTEM
========================================================================
Knowledge Graph
Architecture Decisions
Experiment History
Strategy History
Feature History
Model Registry
Artifact Registry
Documentation
Lessons Learned

========================================================================
                 CONTINUOUS LEARNING
========================================================================
Production Metrics
↓
Performance Drift
↓
Feature Drift
↓
Model Drift
↓
Strategy Drift
↓
Weakness Detection
↓
Research Suggestions
↓
New Experiments
↓
Scientific Validation
↓
Deployment

---

## 3. Strategy Architecture & Taxonomy

### 3.1 Strategy Capability Contract
Every strategy MUST expose strict `Consumes` and `Produces` contracts to prevent hidden dependencies.
- **Consumes**: Required Features, Required Concepts, Required Primitive Signals, Required Geometry, Required Sessions, Required Market State, Required Liquidity, Required Regime.
- **Produces**: Trade Candidate, Expected Hold, Stop, Target, Risk, Confidence, Evidence Request.

### 3.2 Universal Query Engine
The architecture centralizes all query logic into one platform-wide Universal Query Engine. Instead of distinct filters per engine, all research queries and dashboards use the same engine, supporting:
`Search, Filter, Sort, Rank, Aggregate, Group, Export`.
Filterable dimensions include: `Market, Exchange, Asset class, Symbol, Timeframe, Session, Regime, Strategy family, Methodology, Concept, Feature, Evidence score, Confidence score, Risk score, Liquidity, Volatility, Date range, Version`.

### 3.3 Unified Scoring Framework
Standardize scores across all modules. Every analytical object exposes, where applicable:
`Confidence, Quality, Reliability, Completeness, Importance, Risk, Freshness, Stability`.

---

## 4. Repository Organization
AlphaGrid
│
├── Foundation
├── Infrastructure
├── Shared
├── Database
├── Backend
│   ├── Market
│   ├── Features
│   ├── PriceGeometry
│   ├── Concepts
│   ├── Methodology
│   ├── Signals
│   ├── Decision
│   ├── Strategies
│   ├── Research
│   ├── Portfolio
│   ├── Risk
│   ├── Execution
│   ├── AI
│   ├── Integrations
│   │   └── vibe_trading
│   ├── Monitoring
│   └── API
│
├── Frontend
├── CLI
├── Tests
├── Documentation
└── Scripts

---

## 5. Development Workflow & Implementation Contract

Your goal is an institutional-grade trading platform, not a collection of completed phases. That means the implementation process itself must be production-grade.

### 5.1 Mandatory Implementation Contract
Every phase MUST execute the following formal sequence. Nothing moves forward until the previous step passes:
`Architecture Review -> Capability Audit -> Gap Analysis -> Impact Analysis -> Implementation -> Repository Integration -> End-to-End Pipeline Validation -> Category A Validation -> Architecture Review -> Repository Freeze -> Next Phase`

### 5.2 End-to-End Means REAL CODE
There should never be a fake pipeline, mocked runtime, simulated DTOs, handcrafted outputs, or fake signals unless the phase explicitly requires stubs because downstream systems literally don't exist.
Every layer must execute the actual production implementation against real or deterministic market data.

### 5.3 Modifying Previous Phases
Previous phases MAY be modified. Institutional systems evolve. If a later phase discovers that an earlier DTO, API, Config, or Test must be changed, it is permitted. However, previous phases may be modified **only through controlled impact analysis and regression validation**.

### 5.4 Mandatory Impact Analysis
Before modifying any frozen or existing code, an Impact Report must be generated detailing:
`Modified Files, Affected DTOs, Affected APIs, Affected Config, Affected Registry, Affected Tests, Affected Strategies, Backward Compatibility, Migration Required?, Rollback Plan`.
Only after this report is reviewed can code be modified.

### 5.5 Validation Automation
Instead of relying on memory to execute 30+ tests, the platform uses an automated Validation Engine (`Backend/validation/`). One command (`python validate_phase.py --phase <X>`) executes the entire suite: Repository Audit, Capability Audit, Registry Audit, DTO Audit, Import Audit, E2E Pipeline, Cross-Family Regression, Deterministic Replay, Numerical Robustness, Performance, Memory, Stress, Documentation, and Evidence Generation.

### 5.6 Expanding the End-to-End Pipeline
Every new phase extends the **same** pipeline. You must never create a second pipeline. The pipeline grows from `Market Data -> Strategies` today, out to `Market Data -> ... -> Execution -> Analytics -> Evidence` in the future.

### 5.7 First-Class Artifacts
Configuration schemas, REST APIs, Internal APIs, DTOs, Registries, Capability metadata, Runtime config, Documentation, CLI, and Validation rules are first-class citizens. Any change to them requires the same impact analysis and regression process as code changes.

### 5.8 Production Code Only
No implementation is allowed to exist solely to satisfy tests. Every implementation must be intended for production use. Tests verify production code; production code is never written merely to make tests pass.

### 5.9 Three Levels of Validation
1. **Level 1**: Deterministic replay using fixed historical datasets (Default for every phase).
2. **Level 2**: Integration against real infrastructure (real APIs, databases, brokers where applicable).
3. **Level 3**: Live-market validation in paper trading or sandbox environments.

## 6. Institutional AI & Agentic Orchestration

### 6.1 AI Boundary Rule
AI is strictly advisory and operates exclusively as an evaluation augmentation layer. AI evaluates existing deterministic information.
AI must NEVER:
- Generate trades directly.
- Bypass the deterministic canonical pipeline.
- Promote strategies to production.
- Override validation gates or evidence scores.
- Modify architecture automatically without audits.

When AI exists, the pipeline becomes:
`Strategy Intelligence -> Rule Evaluation + AI Evaluation -> Consensus -> Risk`
*AI augments Strategy Intelligence; it does not replace the deterministic foundation.*

### 6.2 Knowledge Architecture
**Research Knowledge Graph**: One of the strongest parts of the platform. Nodes include Features, Concepts, Signals, Strategies, Methodologies, Datasets, Experiments, Evidence, ADRs.
Relationships explicitly defined: `uses, produces, depends_on, derived_from, validated_by, supersedes, contradicts, supports, trained_on`.

---

## 7. External Intelligence Integration (HKUDS Vibe-Trading)

### 7.1 Objective
Integrate the HKUDS Vibe-Trading repository into AlphaGrid without modifying frozen components or creating architectural conflicts.
The integration must maximize the value obtained from HKUDS Vibe-Trading while ensuring AlphaGrid remains the system of record for research, strategy validation, portfolio management, execution, and governance.

### 7.2 Deferred Integration Rule
When a future phase depends on an external repository, implementation must pause at the beginning of that phase and request the exact repository from the user. The repository is treated as an external dependency until that point. No assumptions, placeholder implementations, or speculative integration are permitted.

### 7.3 Activation Rule (Phase 16 Entry Gate)
External repositories must not be analyzed, cloned, integrated, or modified until the roadmap explicitly reaches their designated implementation phase (currently Phase 16 — Vibe-Trading Integration).
Before that phase:
- No repository inspection.
- No code copying.
- No adapter implementation.
- No assumptions about repository internals.
- No placeholder wrappers.

The only permitted reference is the integration architecture and governance rules.
When the roadmap reaches Phase 16, the implementation must stop and request the official repository:
- Repository URL
- Branch/tag/commit to integrate
- Any local modifications or forks
- Dependency constraints

No implementation begins until the repository is available.

### 7.4 Mandatory Repository Audit
Only after receiving the repository:
1. Clone/download the repository.
2. Audit the complete codebase.
3. Build a module inventory.
4. Identify reusable components.
5. Identify duplicated functionality.
6. Identify conflicting architecture.
7. Produce a compatibility report.
8. Produce an integration plan.
No code is written before this audit is complete.

### 7.5 Repository-First Integration Rule
For every HKUDS file:
- Search AlphaGrid for existing functionality.
- Reuse AlphaGrid implementation whenever possible.
- Reuse HKUDS only when it provides additional value.
- Never duplicate existing capabilities.
- Never replace frozen AlphaGrid components without justification.
- Integrate through adapters only.

### 7.6 Cross-Phase Modification Rule
Integration is allowed to modify previous AlphaGrid phases if necessary, provided:
- The change is required for end-to-end integration.
- Backward compatibility is maintained.
- Canonical pipeline remains valid.
- Existing tests continue to pass.
- New tests are added.
- Documentation is updated.
- Capability Registry is updated.
- Repository Impact Checklist is completed.

No phase is considered isolated; integration may require coordinated changes across configuration, dependency injection, APIs, registries, documentation, and tests.

### 7.7 Adapter Architecture
```text
HKUDS Repository
        │
        ▼
Repository Audit
        │
        ▼
Compatibility Analysis
        │
        ▼
Integration Adapter
        │
        ▼
AlphaGrid Internal APIs
        │
        ▼
Canonical Pipeline
```
HKUDS must never call AlphaGrid internals directly. AlphaGrid must never depend on HKUDS internal modules. Only the adapter layer may communicate between them.

### 7.8 Completion Gate
Phase 16 is complete only when:
- HKUDS repository fully audited.
- Compatibility report completed.
- File-by-file integration completed.
- Repository duplication eliminated.
- All affected AlphaGrid modules updated.
- Canonical pipeline passes.
- Family regression passes.
- End-to-end regression passes.
- Documentation updated.
- Capability Registry updated.
- Production readiness verified.

### 7.4 Stable Dependency Rule (Institutional Governance)
Once a platform successfully passes the Phase Exit Gate and is marked as **Frozen**, it becomes a **Read-Only** Stable Dependency.
No future platform may directly modify a frozen platform to change its behavior.

Instead, if a modification is required, the following institutional process must be observed:
1. **Architecture Change Request (ACR)**: A formal request detailing the needed change.
2. **Repository Impact Analysis**: A scan identifying all downstream consumers that might break.
3. **Classification**: Assessment of the ACR scope.
4. **Human Approval**: The change must be explicitly approved.
5. **Controlled Implementation**: The implementation of the change.
6. **Recertification**: The platform's entire certification suite must be re-run and pass.
7. **Freeze**: The platform is re-frozen.

This guarantees that upstream foundational platforms remain unconditionally stable for downstream dependencies.

### 7.5 Cross-Platform Contract Rule
Each platform MUST publish an immutable contract (specifying its inputs, outputs, version, guarantees, and compatibility). Downstream platforms MUST depend ONLY on these published contracts, rather than any internal implementations of the upstream platform. This preserves platform purity, makes upgrades safer, and simplifies long-term maintenance.

### 7.6 Platform Enhancement Policy
The only legal way to modify a frozen platform is through the formal enhancement lifecycle: Frozen Platform -> Enhancement Proposal -> Repository Scan -> Legacy Classification -> Impact Analysis -> Human Approval -> Implementation -> Regression -> Phase Exit -> Freeze vN+1 -> Repository Evolution Record.
