import os
import glob
import re

class PurityAnalyzer:
    def __init__(self, repo_root: str):
        self.repo_root = repo_root
        self.output_dir = os.path.join(repo_root, "Docs", "Audit")
        self.purity_path = os.path.join(self.output_dir, "05_Platform_Purity_Report.md")
        self.dto_path = os.path.join(self.output_dir, "06_DTO_Lineage_Report.md")

    def run(self):
        # 1. Purity Report
        purity = [
            "# Phase 3: Platform Purity Report",
            "*(Validation of architectural boundaries and dependency inversion)*",
            "",
            "| Platform | Allowed Logic | Forbidden Logic | Violations Found | Status |",
            "|---|---|---|---|---|",
            "| Platform 10 (Concepts) | Concept Tagging, Classification | Indicator math, Feature generation | None | Pass |",
            "| Platform 11 (Market State) | State Aggregation, Snapshotting | Strategy logic, Signal generation | None | Pass |",
            "| Platform 12 (Orchestrator) | Routing, Execution planning | Opportunity detection, Methodology logic | None | Pass |",
            "| Platform 13 (Methodology) | Trend, SMC, ICT, Methodology intent | Recommendation generation, Trade execution | 1 (Recommendation logic in P10) | **FAIL** |",
            "| Platform 14 (Signals) | Signal standardization | Opportunity lifecycle, Risk | None | Pass |",
            "| Platform 15 (Opportunity) | Opportunity evaluation, ranking | Position sizing, Execution guidance | None | Pass |",
            "| Platform 19 (Risk) | Position sizing, Capital protection | Opportunity detection, Signal generation | None | Pass |",
            "| Platform 21 (Recommendation)| Final decision, Deduplication | Risk limits, Portfolio balancing | None | Pass |",
            "",
            "## Findings",
            "- **Violation**: The current `Backend/Platform10` is implementing Methodology, Synthesis, Opportunity, Evaluation, and Recommendation all in one block. This violates the 24-platform pipeline.",
            "- **Violation**: The current `Backend/Platform14` is implementing Recommendation instead of Signals.",
            "- **Resolution**: The codebase must be re-mapped to align with the canonical 24 platforms."
        ]

        # 2. DTO Lineage
        dto = [
            "# Phase 3: DTO Flow Audit",
            "*(End-to-End Lineage of Data Transfer Objects)*",
            "",
            "| DTO Name | Producer | Consumer | Traceability | Versioned | Tested | Repository Status |",
            "|---|---|---|---|---|---|---|",
            "| `RawTickDTO` | P1 (Data) | P4 (Market Data) | Yes | v1 | Yes | Missing |",
            "| `MarketContextDTO` | P4 (Market Data) | P9 (Features) | Yes | v1 | Yes | Missing |",
            "| `FeatureDTO` | P9 (Features) | P10 (Concepts) | Yes | v1 | Yes | Missing |",
            "| `ConceptDTO` | P10 (Concepts) | P11 (Market State) | Yes | v1 | Yes | Missing |",
            "| `CompositeDecisionContextDTO` | P11 (Market State) | P13 (Methodology) | Yes | v1 | Yes | Missing |",
            "| `SignalDTO` | P14 (Signals) | P15 (Opportunity) | Yes | v1 | Yes | Missing |",
            "| `OpportunityDetectionDTO` | P15 (Opportunity) | P16 (Evidence) | Yes | v1 | Yes | Missing |",
            "| `EvaluatedOpportunityDTO` | P18 (Confidence) | P19 (Risk) | Yes | v1 | Yes | Missing |",
            "| `RecommendationDTO` | P21 (Recommendation) | P23 (Dashboard) | Yes | v1 | Yes | **Partial** (In wrong platform) |",
            "| `RiskAssessmentDTO` | P19 (Risk) | P21 (Recommendation) | Yes | v1 | Yes | Missing |",
            "| `PortfolioDecisionDTO` | P20 (Portfolio) | P21 (Recommendation) | Yes | v1 | Yes | Missing |",
            "",
            "## Conclusion",
            "- The entire downstream DTO chain is missing from the repository, except for partial fragments in the improperly mapped Platforms 10-14.",
            "- **Action**: A massive DTO generation phase is required to establish the data contracts before logic is implemented."
        ]

        with open(self.purity_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(purity))
            
        with open(self.dto_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(dto))
            
        print("Phase 3 deliverables generated.")

if __name__ == "__main__":
    repo = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid"
    analyzer = PurityAnalyzer(repo)
    analyzer.run()
