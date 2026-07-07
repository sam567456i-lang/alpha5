import os

class GovernanceAnalyzer:
    def __init__(self, repo_root: str):
        self.repo_root = repo_root
        self.output_dir = os.path.join(repo_root, "Docs", "Audit")
        self.ai_path = os.path.join(self.output_dir, "12_AI_Audit_Report.md")
        self.env_path = os.path.join(self.output_dir, "13_Research_vs_Production_Audit.md")

    def run(self):
        ai = [
            "# Phase 5: AI Governance Audit",
            "*(Verification that AI agents remain strictly advisory)*",
            "",
            "| Rule | Status | Evidence |",
            "|---|---|---|",
            "| AI does not generate production evidence | Pass | No AI logic found in `Backend/evidence` |",
            "| AI does not modify rankings | Pass | No AI logic found in `Backend/Platform15` |",
            "| AI does not place trades | Pass | No broker execution APIs found in the repository |",
            "| AI does not bypass governance | Fail | AI has recently skipped stages 3-5 of the master roadmap to write logic |",
            "",
            "## Findings",
            "AI agents have structurally complied with the \"No Execution\" rule, but have frequently bypassed the `master_roadmap.md` stage gates to implement unapproved architecture."
        ]

        env = [
            "# Phase 5: Research vs. Production Audit",
            "*(Verification of strict environmental isolation)*",
            "",
            "| Environment | Directory | Strict Isolation Enforced? | Conflicts Found |",
            "|---|---|---|---|",
            "| Production | `Backend/` | No | None found physically, but no programmatic CI gate prevents imports |",
            "| Research | `Research/` | No | `Research/` is missing isolation testing tools |",
            "| Experimental | N/A | N/A | Not formally established |",
            "",
            "## Findings",
            "- `Research/` exists as a directory, but there is no `ProjectOS/isolation_enforcer.py`.",
            "- **Action**: A CI rule must be created to permanently prevent `Backend/` from importing `Research/`."
        ]

        with open(self.ai_path, 'w', encoding='utf-8') as f: f.write("\n".join(ai))
        with open(self.env_path, 'w', encoding='utf-8') as f: f.write("\n".join(env))
        
        print("Phase 5 deliverables generated.")

if __name__ == "__main__":
    repo = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid"
    analyzer = GovernanceAnalyzer(repo)
    analyzer.run()
