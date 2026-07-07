import os
from typing import List

class ChangeImpactEngine:
    """Analyzes a set of changed files to determine upstream and downstream impact."""
    def __init__(self, changed_files: List[str]):
        self.changed_files = changed_files
        self.affected_dtos = set()
        self.affected_plugins = set()
        self.affected_registries = set()
        self.affected_platforms = set()
        self.required_regression_suites = set()
        
    def analyze(self) -> str:
        for file in self.changed_files:
            file_lower = file.lower()
            
            # Platform extraction
            if "platform10" in file_lower:
                self.affected_platforms.add("Platform 10 (Methodology)")
            elif "platform11" in file_lower:
                self.affected_platforms.add("Platform 11 (Synthesis)")
            elif "platform12" in file_lower:
                self.affected_platforms.add("Platform 12 (Opportunity)")
            elif "platform13" in file_lower:
                self.affected_platforms.add("Platform 13 (Evaluation)")
            elif "platform14" in file_lower:
                self.affected_platforms.add("Platform 14 (Recommendation)")
                
            # Component extraction
            if "dtos.py" in file_lower:
                self.affected_dtos.add(os.path.basename(os.path.dirname(os.path.dirname(file))) + " DTOs")
            if "plugins" in file_lower:
                self.affected_plugins.add(os.path.basename(file))
            if "registry.yaml" in file_lower:
                self.affected_registries.add("master_capability_registry")
                
        # Downstream cascade rules
        if "Platform 10 (Methodology)" in self.affected_platforms:
            self.required_regression_suites.add("P10")
            self.required_regression_suites.add("P11")
            self.required_regression_suites.add("P12")
            self.required_regression_suites.add("P13")
            self.required_regression_suites.add("P14")
            
        elif "Platform 13 (Evaluation)" in self.affected_platforms:
            self.required_regression_suites.add("P13")
            self.required_regression_suites.add("P14")
            
        self.required_regression_suites.add("End-to-End Decision Pipeline")
        
        return self._format_report()

    def _format_report(self) -> str:
        report = []
        report.append("=== Repository Change Impact Report ===")
        report.append("Changed Files:")
        for f in self.changed_files:
            report.append(f"  - {f}")
        report.append("\nAffected Platforms:")
        for p in self.affected_platforms:
            report.append(f"  - {p}")
        report.append("\nAffected DTOs:")
        for d in self.affected_dtos:
            report.append(f"  - {d}")
        report.append("\nAffected Plugins:")
        for p in self.affected_plugins:
            report.append(f"  - {p}")
        report.append("\nRequired Regression Suites:")
        for s in sorted(list(self.required_regression_suites)):
            report.append(f"  - {s}")
        report.append("=======================================")
        return "\n".join(report)

if __name__ == "__main__":
    # Example usage based on recent changes
    changed = [
        "Backend/Platform14/contracts/dtos.py",
        "Backend/Platform14/plugins/validator.py",
        "master_capability_registry.yaml"
    ]
    engine = ChangeImpactEngine(changed)
    print(engine.analyze())
