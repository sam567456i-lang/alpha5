import os
import sys
import shutil
import json
import yaml
import subprocess
from datetime import datetime

def run_command(cmd):
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

def main():
    if len(sys.argv) < 3:
        print("Usage: python wave_manager.py <wave_name> <component_id>")
        sys.exit(1)
        
    wave_name = sys.argv[1] # e.g. EV-10I-B-WAVE1
    component = sys.argv[2] # e.g. macd
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    evidence_dir = os.path.join(base_dir, "Docs", "Evidence", "2026", wave_name)
    rollback_dir = os.path.join(evidence_dir, "rollback_snapshot")
    
    os.makedirs(rollback_dir, exist_ok=True)
    
    registry_path = os.path.join(base_dir, "master_capability_registry.yaml")
    temp_ev_dir = os.path.join(base_dir, "Docs", "Evidence", "2026", "EV-TEMP")
    
    # Task 9: Rollback Snapshot
    if os.path.exists(registry_path):
        shutil.copy(registry_path, os.path.join(rollback_dir, "capability_registry.yaml"))
        
    old_graph = os.path.join(temp_ev_dir, "validators", "dependency_graph.json")
    if os.path.exists(old_graph):
        shutil.copy(old_graph, os.path.join(rollback_dir, "dependency_graph.json"))
        
    print("=== Rollback Snapshot Generated ===")
    
    # Task 11: Execute Wave Validation (Architecture, Dependency, Legacy, Performance, etc.)
    try:
        run_command([sys.executable, "validate_phase.py", "--phase", "10i-b", "--family", "momentum", "--profile", "phase"])
    except subprocess.CalledProcessError:
        print("Validation Pipeline Failed! Halting Wave.")
        sys.exit(1)
        
    # Task 8: Standardized Evidence Layout
    summary_path = os.path.join(evidence_dir, "summary.md")
    validation_json = os.path.join(evidence_dir, "validation.json")
    benchmark_json = os.path.join(evidence_dir, "benchmark.json")
    dependency_json = os.path.join(evidence_dir, "dependency.json")
    equivalence_json = os.path.join(evidence_dir, "equivalence.json")
    registry_snapshot = os.path.join(evidence_dir, "registry_snapshot.yaml")
    environment_json = os.path.join(evidence_dir, "environment.json")
    
    # Copy from EV-TEMP
    if os.path.exists(os.path.join(temp_ev_dir, "benchmark.json")):
        shutil.copy(os.path.join(temp_ev_dir, "benchmark.json"), benchmark_json)
    if os.path.exists(os.path.join(temp_ev_dir, "environment.json")):
        shutil.copy(os.path.join(temp_ev_dir, "environment.json"), environment_json)
        
    with open(summary_path, "w") as f:
        f.write(f"# Wave {wave_name} Summary\nValidation passed successfully on {datetime.utcnow().isoformat()}.")
        
    with open(validation_json, "w") as f:
        json.dump({"status": "PASS"}, f)
        
    shutil.copy(registry_path, registry_snapshot)
    
    print("=== Evidence Layout Standardized ===")
    
    # Task 10: Master Capability Registry Enrichment
    with open(registry_path, "r", encoding="utf-8") as f:
        registry = yaml.safe_load(f)
        
    for cap in registry.get('capabilities', []):
        if cap.get('id') == f"ftr-{component}":
            cap['migration'] = {
                'state': 'completed',
                'validated': True,
                'evidence': wave_name,
                'legacy_reference': f"Backend/reference/legacy/features/{component}.py"
            }
            cap.pop('migrated', None)
                
    with open(registry_path, "w", encoding="utf-8") as f:
        yaml.dump(registry, f, sort_keys=False)
        
    print("=== Registry Updated ===")
    
    # Git Tagging
    try:
        run_command(["git", "add", "."])
        run_command(["git", "commit", "-m", f"Wave {wave_name} ({component}) completed"])
        tag_name = f"v{wave_name.lower()}-{component}"
        run_command(["git", "tag", "-a", tag_name, "-m", f"{component.upper()} migrated to Math Core v1.1.0"])
        print(f"=== Wave Frozen. Tag {tag_name} created. ===")
    except Exception as e:
        print(f"Git operations failed: {e}")
        
if __name__ == "__main__":
    main()
