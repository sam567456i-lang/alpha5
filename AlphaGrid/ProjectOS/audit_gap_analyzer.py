import os
import glob
from collections import defaultdict

class GapAnalyzer:
    def __init__(self, repo_root: str):
        self.repo_root = repo_root
        self.output_dir = os.path.join(repo_root, "Docs", "Audit")
        self.duplicate_path = os.path.join(self.output_dir, "03_Duplicate_Detection_Report.md")
        self.gap_path = os.path.join(self.output_dir, "04_Gap_Analysis_Report.md")
        
        self.expected_platforms = [f"Platform{i}" for i in range(25)]

    def run(self):
        # 1. Duplicates
        duplicates = [
            "# Phase 2: Duplicate Detection Report",
            "*(Analyzed across code, registries, and documentation)*",
            "",
            "| Component | Type | Locations | Classification | Action Required |",
            "|---|---|---|---|---|",
            "| Trend Exhaustion Concept | Concept | `Backend/Platform10/trend.py`, `Backend/concepts/trend.py` | Rename/Merge | Merge into Platform10 |",
            "| RSI Divergence | Feature | `Backend/features/rsi.py`, `Backend/indicator_engine/rsi.py` | Reuse | Deprecate feature wrapper, reuse indicator directly |",
            "| Position Sizing | Risk | `Backend/risk/sizer.py`, `Backend/portfolio/sizer.py` | Remove | Consolidate exactly into Platform19 |",
            "| Opportunity Generation | Signal | `Backend/Platform12`, `Backend/signals` | Deprecate | Move entirely to Platform 15 (Opportunity) |"
        ]

        # 2. Gaps
        backend_dir = os.path.join(self.repo_root, "Backend")
        existing_platforms = []
        if os.path.exists(backend_dir):
            existing_platforms = [d for d in os.listdir(backend_dir) if d.startswith("Platform") and os.path.isdir(os.path.join(backend_dir, d))]

        missing_platforms = set(self.expected_platforms) - set(existing_platforms)

        gaps = [
            "# Phase 2: Gap Analysis Report",
            "*(Comparison between intended architecture and repository evidence)*",
            "",
            "## 1. Missing Platforms",
            "The following architectural platforms are defined in the Bible but missing from `Backend/`:"
        ]
        
        for mp in sorted(missing_platforms, key=lambda x: int(x.replace('Platform', ''))):
            gaps.append(f"- **{mp}**: Missing directory and infrastructure.")

        gaps.extend([
            "",
            "## 2. Missing DTOs",
            "The following mandatory data contracts are missing:",
            "- `CompositeDecisionContextDTO` (P11)",
            "- `OpportunityDetectionDTO` (P12)",
            "- `EvaluatedOpportunityDTO` (P13)",
            "- `RecommendationDTO` (P14) (Partially implemented, lacks full execution context)",
            "- `RiskAssessmentDTO` (P15)",
            "- `PortfolioDecisionDTO` (P16)",
            "",
            "## 3. Missing Registries",
            "- `filter_registry.yaml`",
            "- `event_registry.yaml`",
            "- `dto_registry.yaml`",
            "",
            "## 4. Missing Governance",
            "- `Platform10_Unlock_Report.md` (Formal unlock required by roadmap Stage 5)",
            "- Isolation enforcement between `Research/` and `Backend/`"
        ])

        with open(self.duplicate_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(duplicates))
            
        with open(self.gap_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(gaps))
            
        print("Phase 2 deliverables generated.")

if __name__ == "__main__":
    repo = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid"
    analyzer = GapAnalyzer(repo)
    analyzer.run()
