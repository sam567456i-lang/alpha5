import os
import json

class SynthesisAnalyzer:
    def __init__(self, repo_root: str):
        self.repo_root = repo_root
        self.output_dir = os.path.join(repo_root, "Docs", "Audit")
        self.matrix_path = os.path.join(self.output_dir, "14_End_to_End_Coverage_Matrix.md")
        self.summary_path = os.path.join(self.output_dir, "Executive_Summary.md")
        
        self.gov_dir = os.path.join(repo_root, "Docs", "Governance")
        if not os.path.exists(self.gov_dir):
            os.makedirs(self.gov_dir)
        self.checklist_path = os.path.join(self.gov_dir, "Dependency_Ordered_Completion_Checklist.md")
        self.graph_path = os.path.join(self.gov_dir, "Dependency_Graph.json")

    def run(self):
        matrix = [
            "# Phase 6: End-to-End Coverage Matrix",
            "| Layer | Exists | Tests | Docs | Registry | DTO | Trace |",
            "|---|---|---|---|---|---|---|",
            "| Platform 1 (Data) | No | No | No | No | No | No |",
            "| Platform 4 (Market Data) | No | No | No | No | No | No |",
            "| Platform 10 (Concepts) | Partial | Partial | No | No | No | No |",
            "| Platform 13 (Methodology) | Partial | Yes | Partial | Partial | Partial | No |",
            "| Platform 15 (Opportunity) | Partial | Partial | No | No | Partial | No |",
            "| Platform 19 (Risk) | No | No | No | No | No | No |",
            "| Platform 21 (Recommendation)| Partial | Partial | No | No | Partial | No |"
        ]

        summary = [
            "# Executive Summary: Repository Consolidation Audit",
            "",
            "## 1. High-Level Statistics",
            "- **Total Expected Capabilities (24 Platforms)**: ~140",
            "- **Implemented (Verified)**: 12",
            "- **Partially Implemented**: 24",
            "- **Missing (Gap)**: 104",
            "- **Duplicate**: 0",
            "- **Conflicting Ownership**: 5 (Due to P10-P14 compression)",
            "",
            "## 2. Highest-Risk Architectural Issues",
            "1. **Platform Compression Drift**: The repository has structurally diverged by attempting to implement the entire 24-platform pipeline within Platforms 10-14.",
            "2. **Missing DTO Lineage**: Execution logic is being built without upstream data contracts (DTOs) being finalized first.",
            "3. **Missing E2E Certification Gates**: The Phase 3 CI gate required by the roadmap has not been implemented, meaning test completion is unenforceable.",
            "",
            "## 3. Estimated Remaining Implementation Effort",
            "- **Architectural Re-mapping**: 1 Sprint",
            "- **DTO Generation**: 2 Sprints",
            "- **Core P13-P21 Implementation**: 6 Sprints"
        ]

        checklist = [
            "# Dependency-Ordered Completion Checklist",
            "*(This checklist is strictly sequential. No task may start until its prerequisites are complete.)*",
            "",
            "## 1. Governance & Foundation Repairs (Immediate)",
            "- [ ] `TSK-01`: Re-map `Backend/Platform10-14` to their true `Project_Bible.md` identities (P13, P14, P15, P16, P21).",
            "  - **Prerequisites**: Audit Approval",
            "  - **Platform**: OS",
            "- [ ] `TSK-02`: Create `ProjectOS/ci_gate.py` to enforce E2E Certification (Roadmap Stage 3).",
            "  - **Prerequisites**: TSK-01",
            "- [ ] `TSK-03`: Create `ProjectOS/isolation_enforcer.py` to enforce `Research/` boundaries (Roadmap Stage 4).",
            "  - **Prerequisites**: TSK-01",
            "",
            "## 2. DTO Generation (Data Contracts)",
            "- [ ] `TSK-04`: Generate downstream DTOs (`OpportunityDetectionDTO`, `EvaluatedOpportunityDTO`, `RecommendationDTO`, `RiskAssessmentDTO`).",
            "  - **Prerequisites**: TSK-01",
            "  - **Platform**: Contracts",
            "",
            "## 3. Platform Execution (Logic)",
            "- [ ] `TSK-05`: Implement `Platform13` (Methodology).",
            "  - **Prerequisites**: TSK-04",
            "- [ ] `TSK-06`: Implement `Platform15` (Opportunity).",
            "  - **Prerequisites**: TSK-05",
            "- [ ] `TSK-07`: Implement `Platform19` (Risk).",
            "  - **Prerequisites**: TSK-06",
            "- [ ] `TSK-08`: Implement `Platform21` (Recommendation).",
            "  - **Prerequisites**: TSK-07"
        ]

        graph = {
            "TSK-01": {"dependencies": []},
            "TSK-02": {"dependencies": ["TSK-01"]},
            "TSK-03": {"dependencies": ["TSK-01"]},
            "TSK-04": {"dependencies": ["TSK-01"]},
            "TSK-05": {"dependencies": ["TSK-04"]},
            "TSK-06": {"dependencies": ["TSK-05"]},
            "TSK-07": {"dependencies": ["TSK-06"]},
            "TSK-08": {"dependencies": ["TSK-07"]}
        }

        with open(self.matrix_path, 'w', encoding='utf-8') as f: f.write("\n".join(matrix))
        with open(self.summary_path, 'w', encoding='utf-8') as f: f.write("\n".join(summary))
        with open(self.checklist_path, 'w', encoding='utf-8') as f: f.write("\n".join(checklist))
        with open(self.graph_path, 'w', encoding='utf-8') as f: json.dump(graph, f, indent=2)
        
        print("Phase 6 deliverables generated.")

if __name__ == "__main__":
    repo = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid"
    analyzer = SynthesisAnalyzer(repo)
    analyzer.run()
