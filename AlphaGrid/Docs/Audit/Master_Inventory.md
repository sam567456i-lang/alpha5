# Master Inventory (Fully Classified)

## Program: AlphaGrid | Project: Infrastructure
### Phase 8.5: State Engine & Streaming Runtime (Status: Planned)
- Capability: **Rolling State Management**
  - Status: Planned
  - Dependencies: Indicator Engine
- Capability: **Streaming State Tracking**
  - Status: Planned
  - Dependencies: Rolling State Management
- Capability: **Indicator Cache**
  - Status: Planned
  - Dependencies: Streaming State Tracking
- Capability: **Warmup Cache**
  - Status: Planned
  - Dependencies: Indicator Cache
- Capability: **Partial Recomputation Engine**
  - Status: Planned
  - Dependencies: Streaming State Tracking
- Capability: **Incremental Updates (EMA, SMA, ATR, MACD, RSI, VWAP)**
  - Status: Planned
  - Dependencies: Streaming State Tracking

## Program: AlphaGrid | Project: Trading Core
### Wave 5: Extremum Family (Status: Planned)
- Capability: **Donchian Channels**
  - Status: Planned
  - Dependencies: Math Core
- Capability: **High/Low Breakout**
  - Status: Planned
  - Dependencies: Math Core
- Capability: **Support/Resistance Levels**
  - Status: Planned
  - Dependencies: Math Core

### Wave 6: Momentum Family (Status: Planned)
- Capability: **RSI (Relative Strength Index)**
  - Status: Planned
  - Dependencies: Math Core
- Capability: **RMA (Running Moving Average)**
  - Status: Planned
  - Dependencies: Math Core
- Capability: **Momentum Engine Base**
  - Status: Planned
  - Dependencies: Indicator Engine

### Wave 7: Volume Family (Status: Planned)
- Capability: **VWAP (Volume Weighted Average Price)**
  - Status: Planned
  - Dependencies: Math Core
- Capability: **OBV (On-Balance Volume)**
  - Status: Planned
  - Dependencies: Math Core
- Capability: **Volume SMA**
  - Status: Planned
  - Dependencies: Math Core
- Capability: **Accumulation/Distribution**
  - Status: Planned
  - Dependencies: Math Core

## Program: AlphaGrid | Project: Advanced Trading Semantics
### Phase 9.1: Concept Layer (Status: Planned)
- Capability: **Semantic Concept Base**
  - Status: Planned
  - Dependencies: Feature Generators

### Phase 9.2: Inference Layer (Status: Planned)
- Capability: **Concept Fusion Engine**
  - Status: Planned
  - Dependencies: Concept Layer

### Phase 9.3: Methodologies (Status: Planned)
- Capability: **Methodology Base**
  - Status: Planned
  - Dependencies: Inference Layer

### Phase 9.4: Signals (Status: Planned)
- Capability: **Signal Generator Base**
  - Status: Planned
  - Dependencies: Methodologies

### Phase 9.5: Declarative Strategies (Status: Planned)
- Capability: **Strategy Orchestrator**
  - Status: Planned
  - Dependencies: Signals

## Program: AlphaGrid | Project: Execution & Risk
### Phase 10: Live Deployment (Status: Planned)
- Capability: **Portfolio Engine**
  - Status: Planned
  - Dependencies: Declarative Strategies
- Capability: **Risk Engine**
  - Status: Planned
  - Dependencies: Portfolio Engine
- Capability: **Execution Engine**
  - Status: Planned
  - Dependencies: Risk Engine

## Program: AlphaGrid | Project: AI & Knowledge Subsystems
### External Integrations (Status: Planned)
- Capability: **Vibe-Trading Integration**
  - Status: Planned
  - Dependencies: Inference Layer
- Capability: **AI Platform Integration**
  - Status: Planned
  - Dependencies: Execution Engine
- Capability: **Knowledge Subsystem (Vector DB/RAG)**
  - Status: Planned
  - Dependencies: AI Platform Integration

## Program: AlphaGrid | Project: Validation & Governance
### Repository Validation (Status: Planned)
- Capability: **Cross-Family Regression Validator**
  - Status: Planned
  - Dependencies: Validation Framework
- Capability: **Concept Validator**
  - Status: Planned
  - Dependencies: Concept Layer
- Capability: **Methodology Validator**
  - Status: Planned
  - Dependencies: Methodologies
- Capability: **Signal Validator**
  - Status: Planned
  - Dependencies: Signals
- Capability: **Strategy Dependency Validator**
  - Status: Planned
  - Dependencies: Declarative Strategies

## Governance & ADRs
- ADR-001-MTF-Alignment (Frozen)
- ADR-002-Validation-Framework (Frozen)
- ADR-003-Ownership-of-expected-bars (Frozen)
- API Freeze Manifest (Frozen)
- Master Capability Registry (Frozen)
- Validation Registry (Frozen)
