# AlphaGrid Architecture Change Log
*Maintained under Permanent Governance Directive Rule 4*

| Date | Version | Decision ID | Summary | Reason | Approval Status |
|------|---------|-------------|---------|--------|-----------------|
| 2026-07-07 | v3.0 | `DEC-001` | Enshrine Permanent Governance Directive | Ensure continuity and prevent architecture drift across AI sessions. | Approved |
| 2026-07-07 | v3.0 | `DEC-002` | Create Master Lifecycle Registry | Enforce 10-stage execution pipeline across environments. | Approved |
| 2026-07-07 | v3.0 | `DEC-003` | Enforce 6-Tier Environment Isolation | Establish physical boundary between Prod, Research, Sandbox, Experimental, Archive, Imported. | Approved |
| 2026-07-07 | v3.0 | `DEC-004` | Centralize Governance Specification | Consolidate 20+ CI gates into a single registry-driven orchestrator. | Approved |
| 2026-07-07 | v3.0 | `DEC-005` | Platform 15 Risk Certification | Implemented P15 logic, dynamic plugins, UUID traceability, and Phase Exit. | Approved |
| 2026-07-07 | v3.0 | `DEC-006` | Platform 16 Portfolio Certification | Scaffolded 10-engine pipeline, created 4 registries, decoupled PortfolioStateDTO from RiskContextDTO. | Approved |
| 2026-07-07 | v3.0 | `DEC-007` | Wave 2 Methodologies | Scoped and implemented ICT and Wyckoff Methodologies under strict SDK versioning, decoupling Concept generation to Platform 9. | Approved |
| 2026-07-07 | v3.0 | `DEC-008` | Wave 3 Methodologies | Implemented Order Flow and Volume Profile methodologies. Extracted temporal expiration out of methodology DTOs into a universal `FreshnessProfileDTO` to maintain generic downstream architectures. | Approved |
| 2026-07-07 | v3.0 | `DEC-009` | Platform 10 Completeness (Wave 4) | Locked Platform 10 architecture by introducing Dual-Level Lineage, comprehensive Concept Registries, topological Concept Relationships, unified Confidence Inheritance, and Wave 4 Methodologies (Macro, Options, ML, Sentiment). Platform 10 is formally frozen. | Approved |
| 2026-07-07 | v3.0 | `DEC-010` | Platform 18 & Governance Manifest | Executed final strict P10 audit. Locked the Decision Intelligence Manifest defining the exact input/output capabilities of every platform. Built Platform 18 to consume Dual-Level Lineage and generate deterministic Presentation-Model-based ExplainabilityReports. | Approved |
| 2026-07-07 | v3.0 | `DEC-011` | Platform 19 Presentation Intelligence | Built Platform 19 to strictly own Semantic Filtering, grouping, and default ranking via `PresentationQueryEngine` and standard subsystems (Scanner, Workspace, Watchlist, Layout). Formalized the `PresentationQueryDTO` to decouple business logic from the frontend (React/iOS). | Approved |

*(New entries must be appended here prior to any architectural modification)*
