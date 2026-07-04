# ADR 007: Platform 5 Universal Taxonomy and Rich Metadata Enforcement

## Status
Approved and Frozen

## Context
As AlphaGrid builds out Platform 5 (Analysis Platform), a simple monolithic execution engine is insufficient. The repository is scaling to 28 distinct analysis families (e.g., Technical, Fundamental, Macro, Quant, Sentiment). Each capability needs extreme operational tracking across multiple dimensions (Dashboard compatibility, AI prompting, Performance benchmarks, Validation sets, and External Dependencies) to allow the Project OS to automatically govern the repository and prevent architectural drift.

## Decision
We establish the Final Platform 5 Architecture based on a heavily parameterized Master Taxonomy.

### 1. Capability IDs and Versioning
Every analysis plugin MUST define a unique Capability ID (e.g., `AN-TECH-TREND-001`), an explicit version number, and its maturity state (e.g., `Prototype`, `Production`, `Deprecated`).

### 2. Multi-Dimensional Metadata
The `AnalysisRegistration` is the absolute single source of truth for Project OS. We will NOT parse Python AST for business logic. The registration must declare:
- **Dependencies**: Required internal indicators, external data streams (Tick, News, Options).
- **Matrix Support**: Allowed markets, timeframes, and trading styles.
- **Explainability**: Standardized 10-question explainability fields (What happened, Why, Evidence, Confidence, Risks, etc.).
- **Validation**: Strict declaration of testing levels (Property, Integration, Golden Dataset).
- **Dashboard & AI**: Specific widget targets (Scanner, Heatmap, Chart) and AI compatibility.

### 3. Multi-Dimensional Scoring
The generic `numeric_score` is deprecated. `AnalysisResult` must now emit specific vectors (Trend, Momentum, Volume, Volatility, Liquidity, Structure, Risk, AI, Overall) allowing the Recommendation Engine to mathematically rank opportunities without parsing strings.

### 4. Implementation Phasing
Platform 5 must be built in this strict order:
- 5A: Governance Lock
- 5B: Core Refactor
- 5C: Existing Migration
- 5D: New Analysis Families

## Consequences
- The Project OS can now mathematically audit the repository for completeness by reading instantiated `AnalysisRegistration` objects.
- It prevents the implementation of signals (BUY/SELL) within the Analysis layer.
- Upfront development overhead increases significantly to build out the metadata structures, but long-term repository maintenance and AI integration become vastly simpler.
