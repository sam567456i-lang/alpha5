import os
import json

OUT_DIR = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Docs\Reports"

class ReportGenerator:
    def __init__(self):
        os.makedirs(OUT_DIR, exist_ok=True)
        
    def write_pair(self, filename_base, data, md_content):
        # JSON
        with open(os.path.join(OUT_DIR, f"{filename_base}.json"), "w") as f:
            json.dump(data, f, indent=2)
        # MD
        with open(os.path.join(OUT_DIR, f"{filename_base}.md"), "w") as f:
            f.write(md_content)

    def generate_all(self, results):
        self.write_pair("Repository_Report", results["repository"], 
                        f"# Repository Report\nStatus: {results['repository']['status']}\nFiles Scanned: {results['repository']['files_scanned']}")
                        
        self.write_pair("Gap_Report", results["gap"], 
                        f"# Gap Report\nPlatform 5 Status: {results['gap']['platform_5_status']}")
                        
        self.write_pair("Dependency_Graph", results["dependency"], 
                        f"# Dependency Graph\nDepends on P05: {', '.join(results['dependency']['dependent_on_P05'])}")
                        
        self.write_pair("Migration_Report", results["migration"], 
                        f"# Migration Report\nNeeds Migration: {', '.join(results['migration']['needs_migration'])}")
                        
        self.write_pair("Compatibility_Report", results["compatibility"], 
                        f"# Compatibility Report\nRequired Validators: {', '.join(results['compatibility']['validators_required'])}")
                        
        rm = results["implementation_roadmap"]
        rm_md = f"# Implementation Roadmap\n\n"
        rm_md += f"## Current Readiness\n{rm['current_readiness']}\n\n"
        rm_md += f"## Critical Path\n"
        for item in rm['critical_path']:
            rm_md += f"- {item}\n"
        rm_md += f"\n## Recommended Sequence\n"
        for item in rm['recommended_sequence']:
            rm_md += f"1. {item}\n"
            
        self.write_pair("Implementation_Roadmap", rm, rm_md)
