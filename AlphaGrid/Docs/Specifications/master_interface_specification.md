---
Document ID: SPEC-001
Title: "Master Interface Specification"
Version: 1.0.0
Governance Version: 1.0.0
Architecture Version: 1.0.0
Phase: 10
Owner: ArchitectureTeam
Category: Specifications
Maturity: "Level 5: Institutionally Frozen"
Implementation Status: Validated
Current Phase: 10
Future Phase: N/A
Last Validated Phase: 10
Review Date: 2026-07-03
Dependencies: []
Referenced By: []
---

# Master Interface Specification

This document defines the canonical Data Transfer Objects (DTOs) and data contracts exchanged between phases in the AlphaGrid platform.

## Architectural Intent
To ensure strict decoupling, layers must only communicate via these defined DTOs. A Strategy must never read a raw Feature value; it must read a ConceptDTO or SignalDTO. A Concept must never read raw Market Data directly; it must read a FeatureDTO or GeometryDTO.

---

## DTO Inheritance Hierarchy

All DTOs follow a strict three-level inheritance chain:

### BaseObject
Contains only identity and versioning. Every object in the platform inherits from this.
```json
{
  "id": "uuid-or-deterministic-hash",
  "schema_version": "1.0.0",
  "created_at": "ISO-8601-timestamp",
  "updated_at": "ISO-8601-timestamp"
}
```

### VersionedObject : BaseObject
Adds ownership and lifecycle tracking.
```json
{
  "owner": "owning_layer_name",
  "producer": "generator_component_id",
  "lifecycle": "ACTIVE",
  "tags": ["crypto", "btc", "trend"]
}
```

### PipelineObject : VersionedObject
Adds observability, lineage, and data integrity for all objects traversing the runtime pipeline.
```json
{
  "trace_id": "request-trace-uuid",
  "correlation_id": "process-correlation-uuid",
  "fingerprint": "semantic-hash",
  "checksum": "cryptographic-payload-hash",
  "quality": 1.0,
  "confidence": 0.95,
  "metadata": {},
  "lineage": {
    "dependencies": []
  }
}
```

---

## Runtime & Infrastructure DTOs

### RuntimeContextDTO : VersionedObject
**Purpose**: Immutable context constructed once at pipeline start and passed to every engine alongside its `PipelineObject` input. Never mutated during execution.
```json
{
  "execution_id": "exec-uuid",
  "market": "Crypto",
  "exchange": "Binance",
  "asset": "BTC/USD",
  "timeframe": "1h",
  "session": "24h",
  "timezone": "UTC",
  "configuration_snapshot": { "checksum": "abc123" },
  "version_snapshot": {},
  "registry_snapshot": {},
  "scheduler_state": {},
  "enabled_switches": ["trend_family", "mean_reversion_family"],
  "execution_mode": "Backtest",
  "pipeline_start_time": "ISO-8601-timestamp"
}
```

### PipelineSnapshotDTO : VersionedObject
**Purpose**: Mandatory reproducibility snapshot for every pipeline execution and research experiment.
```json
{
  "dto_versions": {},
  "feature_versions": {},
  "geometry_versions": {},
  "concept_versions": {},
  "methodology_versions": {},
  "signal_versions": {},
  "strategy_versions": {},
  "registry_versions": {},
  "configuration_version": "1.0.0",
  "git_commit": "a1b2c3d",
  "dependency_lock": "sha256-hash",
  "python_version": "3.11.9",
  "package_versions": {}
}
```

---

## AI Boundary DTOs (Phase 12)
AI must never receive arbitrary pipeline objects directly. The boundary is enforced through these three frozen DTOs.

### AIInputDTO : PipelineObject
**Purpose**: Curated, structured inputs to the AI subsystem.

### AIOutputDTO : PipelineObject
**Purpose**: Structured AI predictions and evaluations.

### AIEvidenceDTO : PipelineObject
**Purpose**: Explainability artifacts produced by AI for the Evidence Engine.

---

## Market Abstraction Interfaces
Exchange-specific and broker-specific code is encapsulated behind a layered adapter hierarchy.

### MarketAdapter
**Purpose**: Normalizes market-level differences (Stocks vs Crypto vs Forex vs Futures).

### ExchangeAdapter
**Purpose**: Encapsulates exchange-specific protocols and data formats.

### BrokerAdapter
**Purpose**: Encapsulates broker-specific order management APIs.

### ExecutionGateway
**Purpose**: Isolates broker APIs from execution logic. The only component that makes external network calls for order routing.

---

## Pipeline DTOs

### 1. MarketDataDTO : PipelineObject
**Owner Layer**: Data Hub (Phase 3)
**Purpose**: Raw or normalized OHLCV and market data passed into the pipeline.

### 2. MarketIntelligenceDTO : PipelineObject
**Owner Layer**: Market Intelligence (Phase 4)
**Purpose**: Processed macro, breadth, session, liquidity, and corporate action intelligence.

### 3. FeatureDTO : PipelineObject
**Owner Layer**: Feature Store (Phase 5)
**Purpose**: Atomic, purely mathematical time-series calculations.
```json
{
  "symbol": "BTC/USD",
  "timeframe": "1h",
  "values": { "value": 62450.50 }
}
```

### 4. GeometryDTO : PipelineObject
**Owner Layer**: Geometry (Phase 6)
**Consumes**: `MarketDataDTO`, `FeatureDTO`, `MarketIntelligenceDTO`
**Purpose**: Structural and spatial market elements (pivots, swings, channels). Consumes Market Intelligence for session-awareness and Market Data directly for OHLCV-native algorithms.
```json
{
  "symbol": "BTC/USD",
  "type": "SWING_HIGH",
  "price": 63000.00,
  "bar_index": 15420
}
```

### 5. ConceptDTO : PipelineObject
**Owner Layer**: Concept (Phase 7)
**Purpose**: Semantic abstractions (Bullish/Bearish, Overbought/Oversold).
```json
{
  "concept_type": "EXTREMUM",
  "state": "OVERBOUGHT"
}
```

### 6. MethodologyDTO : PipelineObject
**Owner Layer**: Methodology (Phase 8)
**Purpose**: Evaluation of a trading paradigm applied against current concepts.
```json
{
  "is_active": true,
  "direction": 1
}
```

### 7. SignalDTO : PipelineObject
**Owner Layer**: Signal (Phase 9)
**Purpose**: Actionable primitive trading signal prior to strategy weighting.
```json
{
  "direction": 1,
  "signal_type": "MEAN_REVERSION_LONG"
}
```

---

## Post-Strategy Decision Pipeline

The output from Strategy to Execution is strictly delineated into six distinct responsibilities. Each engine has exactly one input DTO and one output DTO.

### 8. StrategyDTO : PipelineObject
**Owner Layer**: Strategy (Phase 10)
**Purpose**: Raw, unvalidated intent/candidate trade from a single strategy.
```json
{
  "action": "BUY",
  "metadata": { "parameters_used": {"fast_period": 20} }
}
```

### 9. DecisionCandidateDTO : PipelineObject
**Owner Layer**: Strategy Intelligence (Phase 13)
**Purpose**: Evaluated, ranked, and evidence-backed candidate produced by Strategy Intelligence after benchmarking, ranking, and evidence gathering.
```json
{
  "candidates": ["strat-cand-1", "strat-cand-2"],
  "ranking": [1, 2],
  "evidence": { "supporting_concepts": 3, "conflicting": 0 },
  "consensus_action": "BUY"
}
```

### 10. DecisionDTO : PipelineObject
**Owner Layer**: Decision Engine (Phase 13)
**Purpose**: Final consensus selection after conflict resolution and optional AI validation.
```json
{
  "action": "BUY"
}
```

### 11. RiskDecisionDTO : PipelineObject
**Owner Layer**: Risk Intelligence (Phase 14)
**Purpose**: Approved trade adjusted for portfolio margin, sizing, and risk constraints.
```json
{
  "action": "BUY",
  "adjusted_quantity": 1.25,
  "risk_limits": { "max_loss": 500 }
}
```

### 12. ExecutionPlanDTO : PipelineObject
**Owner Layer**: Execution Intelligence (Phase 16)
**Purpose**: The planned execution approach (TWAP, VWAP, Iceberg, broker routing) before actual broker submission.
```json
{
  "algorithm": "VWAP",
  "slices": 10,
  "broker": "primary",
  "urgency": "low"
}
```

### 13. ExecutionDTO : PipelineObject
**Owner Layer**: Execution Intelligence (Phase 16)
**Purpose**: Finalized order result enriched with TCA and slippage data post-fill.
```json
{
  "symbol": "BTC/USD",
  "side": "BUY",
  "quantity": 1.25,
  "status": "FILLED",
  "analytics": { "slippage": 0.01, "latency_ms": 45 }
}
```

---

## Contract Versioning Rules
1. **Semantic Versioning**: All DTOs adhere strictly to Semantic Versioning (`MAJOR.MINOR.PATCH`).
2. **Backward Compatibility**: Adding a new field to a DTO's `metadata` or `values` dictates a `MINOR` bump.
3. **Breaking Changes**: Modifying a required root field, changing a data type, or altering the semantic meaning of an existing field dictates a `MAJOR` bump.
4. **CI Enforcement**: Changing a DTO contract without a corresponding migration script and version bump must fail CI.
