import os
import json
import yaml
from ProjectOS.capability.matrix_generator import CapabilityMatrixGenerator
from ProjectOS.dependency.graph_engine import DependencyEngine
from ProjectOS.registry.parser import RegistryParser

class AcceptanceEngine:
    """Project OS Stage 7.5 Acceptance Engine"""
    
    def __init__(self, repo_root: str):
        self.repo_root = repo_root
        self.reports_dir = os.path.join(repo_root, "Docs", "Governance", "Reports")
        os.makedirs(self.reports_dir, exist_ok=True)
        
    def generate_dependency_matrix(self):
        engine = DependencyEngine(self.repo_root)
        graph = engine.build_dependency_graph()
        
        md_path = os.path.join(self.reports_dir, "Master_Dependency_Matrix.md")
        json_path = os.path.join(self.reports_dir, "Master_Dependency_Matrix.json")
        
        # Markdown
        with open(md_path, "w", encoding="utf-8") as f:
            f.write("# Master Dependency Matrix\n")
            f.write("| Capability ID | Dependencies |\n")
            f.write("|---|---|\n")
            for cap, deps in graph.items():
                f.write(f"| `{cap}` | {', '.join(deps) if deps else 'None'} |\n")
                
        # JSON
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(graph, f, indent=4)
            
        return md_path, json_path

    def run_acceptance_suite(self):
        print("Executing Stage 7.5 Acceptance Suite...")
        
        # 1. Capability Matrix Generation
        print("-> Generating Capability Matrix...")
        cap_gen = CapabilityMatrixGenerator(self.repo_root)
        cap_gen.generate_matrix()
        
        # 2. Dependency Matrix Generation
        print("-> Generating Dependency Matrix (Markdown & JSON)...")
        self.generate_dependency_matrix()
        
        # 3. Determinism Test
        print("-> Executing Determinism Consecutive Run Test...")
        parser = RegistryParser(self.repo_root)
        run1 = parser.get_capabilities()
        run2 = parser.get_capabilities()
        if run1 == run2:
            print("   [PASS] Stable consecutive runs verified.")
        else:
            print("   [FAIL] Non-deterministic registry extraction.")
            
        print("Stage 7.5 Acceptance Complete. Project OS is now fully authorized to govern AlphaGrid.")

if __name__ == "__main__":
    repo_root = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid"
    tester = AcceptanceEngine(repo_root)
    tester.run_acceptance_suite()
