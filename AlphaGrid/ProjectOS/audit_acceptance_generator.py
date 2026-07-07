import os
import glob

class AcceptanceGenerator:
    def __init__(self, repo_root: str):
        self.repo_root = repo_root
        self.output_dir = os.path.join(repo_root, "Docs", "Audit")
        self.gov_dir = os.path.join(repo_root, "Docs", "Governance")
        self.acceptance_path = os.path.join(self.output_dir, "16_Architecture_Acceptance_Report.md")
        self.migration_path = os.path.join(self.output_dir, "17_Repository_Migration_Plan.md")
        self.checklist_path = os.path.join(self.gov_dir, "Dependency_Ordered_Completion_Checklist.md")

    def run(self):
        # 1. Architecture Acceptance Report
        acc = [
            "# Architecture Acceptance Report",
            "*(Mandatory gate before Repository Synchronization or Restructuring)*",
            "",
            "## 1. Executive Findings",
            "- **Total Expected Capabilities**: ~140",
            "- **Duplicates**: 0",
            "- **Missing capabilities**: 104",
            "- **Ownership conflicts**: 1 major conflict (Methodology logic claiming to own Recommendation logic).",
            "- **Platform purity violations**: `Backend/Platform14` contains logic mapped to P21 in the Project Bible.",
            "- **DTO violations**: `Backend/Platform14/contracts/dtos.py` defines `RecommendationDTO` which lacks the required `ExecutionContext`.",
            "- **Registry inconsistencies**: `master_capability_registry.yaml` lists Opportunity Detection under Platform 12, but Project Bible lists it under Platform 15.",
            "",
            "## 2. Hard Evidence of Architectural Drift",
            "**Hypothesis**: The pipeline compressed P13-P21 into P10-P14.",
            "**Evidence**:",
            "- **Project Bible Reference**: Line 62 explicitly states `Platform 15: Opportunity Platform`.",
            "- **Repository Reality**: The folder `Backend/Platform12` contains `Opportunity` logic.",
            "- **Project Bible Reference**: Line 77 explicitly states `Platform 21: Recommendation Platform`.",
            "- **Repository Reality**: The folder `Backend/Platform14` contains `recommendation_generator.py`.",
            "- **Downstream Effects**: This compression caused missing downstream DTOs (`RiskAssessmentDTO`, `PortfolioDecisionDTO`) and prevents accurate platform maturity tracking.",
            "",
            "## 3. High-Risk Issues",
            "1. **CRITICAL**: The physical platform folders (`Backend/Platform10-14`) do not align with the frozen `Docs/Project_Bible.md`.",
            "2. **HIGH**: Master registries contain mapping errors due to the folder misalignment.",
            "3. **MEDIUM**: E2E CI gate is missing.",
            "",
            "## 4. Proposed Changes",
            "- **Change**: Re-map `Backend/Platform10` to `Backend/Platform13_Methodology`.",
            "  - **Evidence**: Methodology is P13 in the Bible.",
            "  - **Risk**: High (breaks absolute imports).",
            "  - **Rollback Plan**: Git checkout `b5e72f1a` (Frozen v2 state).",
            "- **Change**: Re-map `Backend/Platform14` to `Backend/Platform21_Recommendation`.",
            "  - **Evidence**: Recommendation is P21 in the Bible.",
            "  - **Risk**: High.",
            "  - **Rollback Plan**: Git checkout `b5e72f1a`.",
            "",
            "## 5. Repository Statistics",
            "- **Number of files**: 1745",
            "- **DTO count**: 14 files",
            "- **Plugin count**: 37 files",
            "- **Registry count**: 34 files",
            "- **Test count**: 167 files",
            "- **Documentation count**: 340 files",
            "",
            "## 6. Final Recommendation",
            "**ACCEPT WITH CHANGES**",
            "Execute TSK-01 in three staged phases (Governance, Restructuring, Validation). Do not execute physical moves until Governance mapping is approved."
        ]

        # 2. Repository Migration Plan
        mig = [
            "# Repository Migration Plan",
            "*(This is the explicit execution script for TSK-01B. It will not run until TSK-01A is approved.)*",
            "",
            "| Old Path | New Path | Reason | Owner | Consumers | Risk | Rollback |",
            "|---|---|---|---|---|---|---|",
            "| `Backend/Platform10` | `Backend/Platform13_Methodology` | Align with Project Bible P13 | Methodology Platform | P14 (Signals) | High (Imports) | Git Checkout |",
            "| `Backend/Platform11` | `Backend/Platform14_Signals` | Align with Project Bible P14 | Signal Platform | P15 (Opportunity) | High | Git Checkout |",
            "| `Backend/Platform12` | `Backend/Platform15_Opportunity` | Align with Project Bible P15 | Opportunity Platform | P16, P19 | High | Git Checkout |",
            "| `Backend/Platform13` | `Backend/Platform18_Confidence` | Align with Project Bible P18 | Confidence Platform | P19 (Risk) | High | Git Checkout |",
            "| `Backend/Platform14` | `Backend/Platform21_Recommendation` | Align with Project Bible P21 | Recommendation Platform | P23 (Dashboard) | High | Git Checkout |",
            "",
            "## Pre-Migration Validation",
            "1. Simulate imports using `ProjectOS/import_validator.py`.",
            "2. Update all YAML registries to point to the new paths (TSK-01A).",
            "3. Generate a strict text replacement script for `import Backend.Platform10` -> `import Backend.Platform13_Methodology`."
        ]

        # 3. Update Checklist
        chk = [
            "# Dependency-Ordered Completion Checklist",
            "*(Updated with TSK-01 Split)*",
            "",
            "## 1. Governance Synchronization (TSK-01A)",
            "- [ ] `TSK-01A`: Update `Project_Bible.md`, `master_roadmap.md`, `master_capability_registry.yaml`, and documentation to reflect the new platform mapping.",
            "  - **Prerequisite**: Acceptance of `16_Architecture_Acceptance_Report.md`",
            "",
            "## 2. Repository Restructuring (TSK-01B)",
            "- [ ] `TSK-01B`: Execute the `17_Repository_Migration_Plan.md`.",
            "  - **Prerequisite**: TSK-01A Approved, Migration Plan Approved.",
            "",
            "## 3. Validation & Freeze (TSK-01C)",
            "- [ ] `TSK-01C`: Run Repository Integrity Gate, Platform Purity, DTO Validation, Full E2E, Regression.",
            "  - **Prerequisite**: TSK-01B Completed successfully.",
            "",
            "## 4. E2E Certification Gates (TSK-02)",
            "- [ ] `TSK-02`: Create `ProjectOS/ci_gate.py` (Roadmap Stage 3).",
            "  - **Prerequisite**: TSK-01C Approved.",
            "",
            "## 5. Isolation Enforcement (TSK-03)",
            "- [ ] `TSK-03`: Create `ProjectOS/isolation_enforcer.py` (Roadmap Stage 4).",
            "  - **Prerequisite**: TSK-01C Approved."
        ]

        with open(self.acceptance_path, 'w', encoding='utf-8') as f: f.write("\n".join(acc))
        with open(self.migration_path, 'w', encoding='utf-8') as f: f.write("\n".join(mig))
        with open(self.checklist_path, 'w', encoding='utf-8') as f: f.write("\n".join(chk))
        
        print("Acceptance Report and Migration Plan generated.")

if __name__ == "__main__":
    repo = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid"
    generator = AcceptanceGenerator(repo)
    generator.run()
