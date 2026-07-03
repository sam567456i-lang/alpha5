---
Document ID: KNOW-004
Title: "AlphaGrid Master Rulebook"
Version: 1.0.0
Governance Version: 1.0.0
Architecture Version: 1.0.0
Phase: 10
Owner: ArchitectureTeam
Category: Knowledge
Maturity: "Level 5: Institutionally Frozen"
Implementation Status: Validated
Current Phase: 10
Future Phase: N/A
Last Validated Phase: 10
Review Date: 2026-07-03
Dependencies: []
Referenced By: []
---

# AlphaGrid Master Rulebook

This document is a definitive compilation of every architectural, engineering, and operational rule discussed throughout the entire chat. 

---

## 1. Architectural Core Principles

### 1.1 Architectural Dependency Rule
Every Program must explicitly declare its boundaries to prevent architectural shortcuts.
- **Consumes**: Required upstream inputs.
- **Produces**: Outputs generated.
- **Allowed Downstream**: Permitted consumers of the output.
- **Forbidden Downstream**: Layers that must NEVER directly consume this output.

### 1.2 Single Source of Truth Rule (Contract Ownership)
Every responsibility, contract, and domain must have exactly one authoritative owner. Never allow duplicate implementations.

### 1.3 Universal Engine Contract
Every engine across the entire platform MUST implement an identical architectural contract. The metadata must expose:
`Engine ID, Version, Owner, Registry, Consumes, Produces, Dependencies, Configuration schema, Lifecycle state, Fingerprint, Quality metadata`.

### 1.4 Canonical Object Rule
Every canonical object flowing through the pipeline must expose consistent baseline metadata:
`ID, Version, Owner, Timestamp, Fingerprint, Confidence, Quality, Lineage, Lifecycle`.

### 1.5 Research Object Lineage
Every research object carries immutable lineage, allowing complete traceability from a trade recommendation back to originating market data.

### 1.6 Canonical Consume Rule
A stage is NOT complete merely because it produced output. A stage is ONLY considered complete when its output is successfully consumed by the immediate downstream stage during a canonical execution.

### 1.7 Strategy Capability Contract
Every strategy MUST expose strict `Consumes` and `Produces` contracts to prevent hidden dependencies.

### 1.8 AI Boundary Rule
AI is strictly advisory. AI must NEVER: promote strategies to production, override validation gates, modify architecture automatically without audits, or bypass canonical pipeline execution.

---

## 2. Engineering & Validation Rules

### 2.1 Repository Impact & Extension Rule (MANDATORY)
Every implementation must begin with a repository impact analysis. When adding a new phase, engine, or capability, the implementation must evaluate and update the **17 integration points**:
`Configuration, Models, Contracts, Registry, Factory, Plugin Discovery, DI, Bootstrap, Canonical Pipeline, Event Bus, Persistence, Metrics, Audit, API, Dashboard, Documentation, Tests`.

### 2.2 No Isolated Features Rule
Nothing may exist independently. When adding a Feature, Concept, Methodology, Strategy, AI Model, CLI, or API, the implementation must update every downstream layer automatically: `Registry -> DI -> Config -> Strategy -> API -> CLI -> Tests -> Documentation -> Capability Matrix`.

### 2.3 Production Acceptance Gate & End-to-End Completion
A phase is complete ONLY if the strict 17-step sequence is achieved, including: `Repository Audit -> Unit/Integration Tests -> Canonical Replay -> Real Production Code -> Real Dataset -> Output Consumed -> Manifest Generated -> Evidence Frozen -> Cursor Updated`.

### 2.4 Institutional Code Generation & Testing Standards
Every implementation must be written for production.
- **Code Quality:** Complete implementation, no placeholders, no fake implementations, no TODOs, no FIXMEs. End-to-end integrated, strongly typed, deterministic.
- **Testing Standards:** No mocks, no stubs, no bypasses. Tests must run against real code and real datasets.
- **Requirements:** Structured logging, dependency injection, validation, monitoring.

### 2.5 Universal Registries
Every extensible subsystem MUST follow the exact same registration model: `Registry, Factory, Plugin discovery, Metadata, Versioning, Health, Configuration, Enable/Disable, Audit`.

### 2.6 Interface Verification Rule
Before invoking a downstream consumer, automatically verify: `Schema, Version, Ownership, Nullability, Required fields, Cardinality, Quality score, Confidence, Lineage, Fingerprint, Compatibility`. Fail pipeline if any check fails.

### 2.7 Interface Evolution & Backward Compatibility
Changes to public/Stable interfaces must be `versioned, migrated, documented, and regression tested`. Whenever ANY file changes, automatically verify all existing APIs, Config, DTOs, and Tests. Nothing may silently break.

### 2.8 No Hidden Dependencies Rule
Every engine must explicitly declare all required inputs. No engine may depend on Globals, Singleton state, Implicit caches, or Hidden configurations.

### 2.9 Family-Level & Layer Integration Tests
- **Family-Level Testing:** Test strategy families (e.g., all trend strategies), then the entire platform together.
- **Layer Integration Tests:** Every layer must have its own E2E verification (e.g., `Market -> Strategy`, then `Strategy -> MonteCarlo`).

### 2.10 Multi-Level Testing Pyramid
Institutional-grade verification: `Unit -> Component -> Module -> Family -> Integration -> Regression -> Scientific -> Performance -> Stress -> Long-duration -> End-to-End -> Production Simulation`.

### 2.11 Repository Audit Rule
Before coding: `Search repository -> Find reusable code -> Compare architecture -> Reuse -> Extend -> Create new only if necessary`. Never duplicate code.

### 2.12 Institutional Code Review Rule
Review for Architecture, Performance, Memory, Concurrency, Scalability, Security, Testing, Documentation, Repository Impact, Technical Debt, and Future Maintainability.

### 2.13 Canonical Pipeline Rule
Every new capability must pass through the full pipeline, from `Raw Data` down to `Execution`. No shortcuts.

### 2.14 Future-Proof Rule
Every new module must be designed so future phases extend it rather than rewrite it.

### 2.15 HKUDS Vibe-Trading Rule
Never copy the HKUDS repository blindly. Execute: `Repository Audit -> Compatibility Matrix -> Reuse AlphaGrid -> Adapter Layer -> Repository Validation -> Integration Tests -> Performance Tests -> Documentation`.

### 2.16 AI Development Rules
Every AI-generated implementation must inspect the repository first, reuse existing code, produce production-quality code, avoid placeholders, update all affected files, and verify backward compatibility.

---

## 3. Operational Standards

### 3.1 Canonical Runtime Contract
Every canonical execution must automatically record exact telemetry: `Input type, Input version, Input checksum, Input count, Runtime, Memory, Output type, Output checksum, Output count, Downstream consumer, Contract verification status, Pass/Fail`.

### 3.2 Pipeline Version Rule
Every canonical execution must record the full architectural signature: `Pipeline Version, Architecture Version, ADR Version, Program Version, Registry Version`.

### 3.3 Deterministic Replay Rule
Any canonical execution MUST be exactly reproducible given the Configuration, Dataset, Code revision, Pipeline version, Plugin versions, and Random seed.

### 3.4 Runtime Authenticity Rule
A run is NOT considered verified unless it satisfies requirements including: Real production code, Real dependency injection, Real registries, and Real datasets. *Bypassing the provider layer or mocking services is strictly forbidden.*

### 3.5 Architecture Drift Rule
The build system must automatically detect architectural drift and fail the build if Registries, Factories, Contracts, or Tests are missing.

### 3.6 Performance Budget Rule
Every engine should declare measurable budgets (Latency, Memory, Throughput) which become strict components of regression testing.

### 3.7 Pipeline Execution Manifest
Every execution automatically generates a Manifest tracking the exact state of each layer, directing engineers to the exact recovery cursor.

### 3.8 Observability Contract
Logging is insufficient. The platform requires Structured logs, Distributed Tracing, Metrics, Health endpoints, and Alerting. Generic logging is forbidden.
