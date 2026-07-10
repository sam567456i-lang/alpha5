---
Authority: Level 1
Parent: Docs/Governance/Constitution.md
Children: None
Supersedes: None
Version: 1.0.0
Status: ACTIVE
---

# Architecture Fitness Functions

To prevent architectural drift and degradation, AlphaGrid relies on automated CI gates. These fitness functions must pass before any code is merged into the master branch.

## 1. Automated Checks

1. **Layer Violations:** Ensures that higher layers (e.g., Layer 2) do not depend on lower layers inappropriately, and that lateral platforms don't bypass dependencies.
2. **SDK Bypasses:** Scans for direct imports of internal database models or memory structures by consumer platforms (e.g., P15 must use `MethodologySDK`, not import `SequenceEvaluator`).
3. **Cyclic Dependencies:** Validates the dependency graph is perfectly acyclic.
4. **Registry Consistency:** Ensures every capability in the codebase exists in the Capability Matrix.
5. **Provenance Completeness:** Checks that all emitted evidence and interpretations contain valid, traceable `Identity` objects linked to their origin.
6. **Immutability Enforcement:** Scans for standard mutable structures (e.g., native `list` or `dict`) in core evidence DTOs, enforcing `frozen=True` dataclasses.
7. **Replay Determinism:** Automatically runs a historical simulation twice and hashes the outputs to ensure bit-for-bit equality.
8. **Configuration Schema Validation:** Ensures all profiles (e.g., `ict_2022.yaml`) parse strictly against the Profile Schema.
9. **Capability Ownership Uniqueness:** Verifies that no two engines or rules claim ownership of the same output evidence type.
10. **Dependency Graph Acyclicity:** Ensures the topological sort of methodologies and engines is valid.
