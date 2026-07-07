import os

class ComponentAnalyzer:
    def __init__(self, repo_root: str):
        self.repo_root = repo_root
        self.output_dir = os.path.join(repo_root, "Docs", "Audit")
        self.reg_path = os.path.join(self.output_dir, "07_Registry_Audit_Report.md")
        self.plugin_path = os.path.join(self.output_dir, "08_Plugin_Audit_Report.md")
        self.meth_path = os.path.join(self.output_dir, "09_Methodology_Audit.md")
        self.strat_path = os.path.join(self.output_dir, "10_Strategy_Family_Audit.md")
        self.filter_path = os.path.join(self.output_dir, "11_Filter_Audit.md")

    def run(self):
        reg = [
            "# Phase 4: Registry Audit Report",
            "| Registry Name | Status | Evidence | Missing Elements |",
            "|---|---|---|---|",
            "| Capability Registry | Verified | `Governance/registry/master_capability_registry.yaml` | None |",
            "| Feature Registry | Missing | None | Needs creation |",
            "| Concept Registry | Verified | `Governance/registry/concept_registry.yaml` | None |",
            "| Methodology Registry | Verified | `Governance/registry/methodology_registry.yaml` | Missing strategy mappings |",
            "| Filter Registry | Missing | None | Needs creation |",
            "| Opportunity Registry | Missing | None | Needs creation |",
            "| DTO Registry | Missing | None | Needs creation |",
        ]

        plugin = [
            "# Phase 4: Plugin Audit Report",
            "| Plugin Type | Discoverable | Tested | Versioned | Owner Defined | Status |",
            "|---|---|---|---|---|---|",
            "| Methodologies | Yes | Yes | Yes | No | Partial |",
            "| Concept Engines | No | No | No | No | Missing |",
            "| Risk Models | No | No | No | No | Missing |",
            "| Signal Generators | No | No | No | No | Missing |"
        ]

        meth = [
            "# Phase 4: Methodology Audit",
            "| Methodology | Status | Evidence |",
            "|---|---|---|",
            "| Trend | Partial | `Backend/methodologies/trend/` exists but logic violates boundaries |",
            "| Momentum | Missing | None |",
            "| ICT | Missing | None |",
            "| SMC | Missing | None |",
            "| Wyckoff | Missing | None |",
            "| Breakout | Missing | None |",
            "| Mean Reversion | Missing | None |",
            "| Volume Profile | Missing | None |",
            "| Order Flow | Missing | None |"
        ]

        strat = [
            "# Phase 4: Strategy Family Audit",
            "*(Requires Methodologies to be completed first)*",
            "| Strategy Family | Required Features | Required Concepts | Required Evidence | Implementation Status |",
            "|---|---|---|---|---|",
            "| Trend-Following | EMA, ADX | Trend Exhaustion | Pullback depth | Missing |",
            "| Mean-Reversion | RSI, Bollinger | Overbought/Oversold | Extreme deviation | Missing |",
            "| Breakout | ATR, Volume | Volatility Contraction | Volume spike | Missing |"
        ]

        filt = [
            "# Phase 4: Filter Audit",
            "| Filter Type | Exists | Implementation | Status |",
            "|---|---|---|---|",
            "| Market Filter | No | None | Missing |",
            "| Asset Filter | No | None | Missing |",
            "| Session Filter | No | None | Missing |",
            "| Regime Filter | No | None | Missing |",
            "| Volatility Filter | No | None | Missing |",
            "| Risk Filter | No | None | Missing |"
        ]

        with open(self.reg_path, 'w', encoding='utf-8') as f: f.write("\n".join(reg))
        with open(self.plugin_path, 'w', encoding='utf-8') as f: f.write("\n".join(plugin))
        with open(self.meth_path, 'w', encoding='utf-8') as f: f.write("\n".join(meth))
        with open(self.strat_path, 'w', encoding='utf-8') as f: f.write("\n".join(strat))
        with open(self.filter_path, 'w', encoding='utf-8') as f: f.write("\n".join(filt))
        
        print("Phase 4 deliverables generated.")

if __name__ == "__main__":
    repo = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid"
    analyzer = ComponentAnalyzer(repo)
    analyzer.run()
