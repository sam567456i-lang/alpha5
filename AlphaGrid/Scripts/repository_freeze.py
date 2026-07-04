import os
import sys
import subprocess

def run_cmd(cmd, desc):
    print(f"=== {desc} ===")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"[FAIL] {desc} failed. Aborting Repository Freeze.")
        sys.exit(1)
    print(f"[PASS] {desc}\n")

def main():
    print("=== INITIATING COMPREHENSIVE REPOSITORY FREEZE ===\n")
    
    # 1. Generate API Freeze Manifest
    run_cmd("python Scripts/generate_api_manifest.py", "API Manifest Generation")
    
    # 2. Update Documentation frontmatter
    # Use the existing script to ensure all evidence has strict metadata
    run_cmd("python Scripts/fix_docs_metadata.py", "Documentation Standardization")
    
    # 3. Execute Full Validation Pipeline (which includes the 29 validators like Roadmap, Registry, Architecture Drift, Math, etc.)
    # We use Phase 10i-c as the final state.
    # The architecture_drift_validator now also enforces the API manifest.
    # The mathematical_validator now asserts Core == Engine == Feature.
    run_cmd('powershell -Command "$env:PYTHONPATH=\'C:\\Users\\praka\\Documents\\Codex\\2026-06-30\\alphagrid-infinity-x-5-0-master\\AlphaGrid\'; python validate_phase.py --phase 10i-c --profile repository"', "Master Validation Pipeline")
    
    # 4. Generate Additional Documentation
    run_cmd("python Scripts/generate_migration_dashboard.py", "Migration Dashboard Generation")
    run_cmd("python Scripts/generate_dependency_graph.py", "Capability Dependency Graph Generation")
    
    # 5. Git Commit & Tag
    print("=== Tagging Architecture Freeze ===")
    print("All validators passed. APIs locked. Generating final git tag...")
    run_cmd("git add .", "Staging files")
    run_cmd('git commit -m "Comprehensive Repository Freeze: All waves completed, APIs locked"', "Committing Freeze")
    run_cmd('git tag -a v10.0.0-rc1-repo-freeze -m "Repository strictly frozen before Phase 9"', "Tagging Release Candidate")
    
    print("\n=== REPOSITORY FREEZE COMPLETE ===")
    print("The repository has been fully audited, locked, documented, and tagged.")
    
if __name__ == "__main__":
    main()
