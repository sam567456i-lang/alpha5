# Dependency-Ordered Completion Checklist
*(Updated with Governance Expansion Tasks)*

## 1. Governance Synchronization (TSK-01A)
- [x] `TSK-01A`: Update `Project_Bible.md` to formally deprecate the 24-platform pipeline and enshrine the canonical P0-P15 pipeline.

## 2. Repository Restructuring (TSK-01B - CANCELLED)
- [x] `TSK-01B`: (Cancelled - Physical folder layout is already correct).

## 3. Validation & Freeze (TSK-01C)
- [x] `TSK-01C`: Run Integrity Gates and DTO Validation against the new P0-P15 Bible.

## 4. Governance Specification (TSK-01.5)
- [x] `TSK-01.5`: Create `ProjectOS_Governance_Specification.md` to define all 20+ CI gates and certification requirements centrally.

## 5. E2E Certification Gates (TSK-02)
- [x] `TSK-02`: Create `ProjectOS/ci_gate.py`. This script must dynamically execute the rules defined in `ProjectOS_Governance_Specification.md` rather than hardcoding checks.

## 6. Isolation Enforcement (TSK-03)
- [x] `TSK-03`: Create `ProjectOS/isolation_enforcer.py`. Implement the 6-tier isolation model (`Production`, `Research`, `Experimental`, `Sandbox`, `Imported`, `Archive`).

## 7. Capability Lifecycle Engine (TSK-04)
- [x] `TSK-04`: Create `master_lifecycle_registry.yaml` and the corresponding ProjectOS validation logic to enforce 10-stage capability lifecycle progression (Draft -> Archived).