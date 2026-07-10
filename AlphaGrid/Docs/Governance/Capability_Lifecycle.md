---
Authority: Level 1
Parent: Docs/Governance/Constitution.md
Children: None
Supersedes: None
Version: 1.0.0
Status: ACTIVE
---

# Capability Readiness Levels (CRL)

This document defines the strict, one-way progression of every capability across Platforms, Programs, and Cross-Cutting Services. The CRL tracking system provides high-fidelity visibility into the maturity of hundreds of concurrent components.

## The CRL Scale

- **CRL-0 (Concept):** An idea logged in the Future Capabilities backlog or via a drafted ADR.
- **CRL-1 (Architecture):** The capability has been structurally validated against the AlphaGrid Constitution and assigned to a Domain and Platform.
- **CRL-2 (Specification):** The `[Family]_Spec.md` document is complete, defining Inputs, Outputs, Dependencies, and Performance targets.
- **CRL-3 (Prototype):** The interfaces (DTOs, SDK contracts) exist, and stubbed logic compiles.
- **CRL-4 (Implemented):** The capability contains business logic and executes unit tests.
- **CRL-5 (Verified):** Proven functionally correct via deterministic simulation (e.g., bit-for-bit replayability).
- **CRL-6 (Production Ready):** Passed all performance benchmarks, stress tests, and integration gates.
- **CRL-7 (Certified):** Meets all analytical and explainability SLAs; formally signed off for live decision-making.
- **CRL-8 (Frozen):** Locked. No further business logic changes allowed.

*(Legacy states like Deprecated and Archived are tracked out-of-band as Status flags, not Readiness levels).*
