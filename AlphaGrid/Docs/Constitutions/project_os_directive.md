# AlphaGrid Infinity X — Stage 1: Project OS Master Implementation Directive (Architecture Freeze v25)

## Mission
This is **NOT** a redesign.
This is **NOT** a roadmap rewrite.
This is **NOT** permission to implement Platform 10 or any downstream production platform.

Your only responsibility is to build **Project OS**, the Repository Operating System for AlphaGrid.
Project OS exists completely outside the production platform hierarchy.
Project OS governs the repository.
It never participates in the trading pipeline, calculates indicators, generates features, concepts, methodologies, signals, opportunities, or recommendations.
Its sole responsibility is repository governance, auditing, validation, planning, certification, and freeze management.

## Absolute Rules
Before writing any code:
Perform complete repository understanding.
Read and validate:
* Master Constitution
* Project Bible
* Master Roadmap
* Platform Manifests
* Capability Registry
* Validation Registry
* Plugin Registry
* Methodology Registry
* Taxonomy Registry
* Universal DTO specifications
* ExecutionContext specification
* ADRs
* Existing documentation, tests, previous audits, freeze reports, and implementation plans.

Nothing may be skipped. Never assume repository contents. Repository evidence overrides documentation.

## Project OS Principles
* Evidence over assumptions.
* Repository is the source of truth.
* Deterministic execution.
* Read-only repository analysis.
* No production code modification during audits.
* Registry-driven behavior.
* Immutable report generation.
* Reproducible outputs.
* Complete traceability.

## Stage 1 — Repository Understanding
Before implementation, Project OS shall build a complete understanding of the repository:
Repository Inventory -> Architecture Inventory -> Governance Inventory -> Registry Inventory -> Platform Inventory -> Capability Inventory -> Dependency Inventory -> Documentation Inventory -> Validation Inventory -> Test Inventory -> Current State Summary
No implementation begins until this phase completes.

## Stage 2 — Repository Audit
Project OS shall perform deterministic repository audits. Minimum audit domains include Repository, Architecture, Governance, Dependencies, Registries, Capabilities, Documentation, Validation, Testing, Coverage, Platform Purity, Architecture Drift, Circular Dependencies, Technical Debt, Duplicate Detection, Dead Code, TODO Inventory, Repository Health, Repository Statistics, Compatibility, Migration Readiness, Platform Readiness, Implementation Readiness, Research Isolation, AI Boundary Validation, Traceability, Replay Readiness, Determinism, Configuration, Universal Switch Readiness, and End-to-End Pipeline Readiness.

## Stage 3 — Repository Normalization
Before any new production implementation, resolve inconsistencies in Documentation, Registry, Naming, Dependency, Architecture, Capability, Validation, and Platform. Repository must be internally consistent before Project OS certification.

## Stage 4 — Project OS Implementation
Create ProjectOS outside Backend.
Suggested structure:
`ProjectOS/cli/`, `core/`, `scanner/`, `repository/`, `governance/`, `registry/`, `taxonomy/`, `dependency/`, `architecture/`, `capability/`, `validator/`, `planner/`, `reporter/`, `certification/`, `freezer/`, `utils/`.
Each module shall own one responsibility only. No monolithic implementation.

## CLI & CI/CD Integration
- CLI: `project_os audit`, `validate`, `certify`, `freeze`, `roadmap`, `report`, `capability-matrix`, `dependency-matrix`, `switches`, `readiness`.
- CI: Enforce validate on PR, certify on Merge, freeze on Release.

## Master Capability Matrix & Dependency Matrix
Project OS shall generate the Master Capability Matrix automatically. Mandatory metadata includes ID, Name, Platform, Program, Project, Family, Plugin, Feature, Concept, Methodology, Signal, Markets, Asset Classes, Exchanges, Timeframes, Trading Styles, Dependencies, Inputs, Outputs, DTO, ExecutionContext, Registry Entry, Validators, Documentation, Dashboard, AI Integration, Research Integration, Notification, Universal Switch, Version, Lifecycle, Status, Freeze State.
Project OS shall generate the complete dependency graph automatically.

## Universal Switch Generation & Report Generation
Project OS shall generate the Universal Switch Registry automatically, supporting extensive scopes and lifecycle states (enabled, disabled, experimental, beta, production, deprecated, frozen). Never hardcode switches.
Generate reports in both Markdown and JSON across extensive domains.

## Certification & Implementation Planning
Project OS shall refuse certification when any mandatory governance gate fails. Certification must stop immediately (no partial).
Project OS shall automatically generate the Implementation Roadmap (Current State -> Missing -> Gap Analysis -> Dependency Resolution -> Critical Path -> Waves -> Risk -> Recommended Next Tasks).

## Final Execution Sequence
1. Repository Understanding
2. Repository Audit
3. Repository Normalization
4. Human Approval
5. Project OS Implementation
6. Project OS Certification
7. Generate Master Capability Matrix
8. Generate Master Dependency Matrix
9. Generate Universal Switch Registry
10. Generate Governance Reports
11. Resolve Governance Gaps
12. Generate Certification Manifest
13. Build End-to-End Certification Framework
14. Create Isolated Research & AI Laboratory
15. Run Full Repository Certification
16. Generate Freeze Report
17. Freeze Repository
18. Unlock Platform 10

## Out of Scope
Do NOT implement Platform 10. Do NOT modify production trading logic. Do NOT redesign the architecture. Do NOT replace existing governance. Do NOT bypass registries. Do NOT bypass Project OS. Focus exclusively on establishing Project OS.
