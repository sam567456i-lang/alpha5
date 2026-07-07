import os
import yaml
import sys

class LifecycleEngine:
    def __init__(self, repo_root: str):
        self.repo_root = repo_root
        self.registry_path = os.path.join(repo_root, "Docs", "Governance", "registry", "master_lifecycle_registry.yaml")
        
        self.valid_stages = [
            "Draft", "Planned", "Scaffolded", "Implemented", "Unit Tested", 
            "Integrated", "Certified", "Frozen", "Deprecated", "Archived"
        ]
        
        # Stages that are strictly forbidden from executing in the Production (Backend/) pipeline
        self.forbidden_in_production = ["Draft", "Experimental", "Deprecated", "Archived"]

    def run(self):
        print("=== AlphaGrid Capability Lifecycle Engine ===\n")
        
        if not os.path.exists(self.registry_path):
            print(f"[FATAL] Lifecycle Registry not found at {self.registry_path}")
            sys.exit(1)
            
        with open(self.registry_path, "r", encoding="utf-8") as f:
            registry = yaml.safe_load(f)
            
        capabilities = registry.get("capabilities", [])
        
        print(f"Loaded {len(capabilities)} tracked capabilities.\n")
        
        violations = 0
        for cap in capabilities:
            name = cap.get("name")
            stage = cap.get("lifecycle_stage")
            env = cap.get("environment")
            
            print(f"Checking: {name} (Stage: {stage}, Env: {env})")
            
            if stage not in self.valid_stages and stage != "Experimental":
                print(f"  [ERROR] Invalid lifecycle stage '{stage}'.")
                violations += 1
                
            if env == "Production" and stage in self.forbidden_in_production:
                print(f"  [FATAL] Capability in '{stage}' stage is illegally assigned to Production environment!")
                violations += 1
            else:
                print("  [PASS]")
                
        print(f"\nTotal Lifecycle Violations: {violations}")
        if violations > 0:
            print("[FAILED] Lifecycle Engine aborted. CI Gate failed.")
            sys.exit(1)
        else:
            print("[SUCCESS] All capabilities conform to lifecycle and isolation constraints.")

if __name__ == "__main__":
    repo = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid"
    engine = LifecycleEngine(repo)
    engine.run()
