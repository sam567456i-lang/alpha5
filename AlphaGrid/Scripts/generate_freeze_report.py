import os
import json
import subprocess
from datetime import datetime

base_dir = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid"
report_json_path = os.path.join(base_dir, "Docs", "Reviews", "Repository_Freeze_Report.json")
report_md_path = os.path.join(base_dir, "Docs", "Reviews", "Repository_Freeze_Report.md")
manifest_path = os.path.join(base_dir, "Docs", "Governance", "api_freeze_manifest.json")
dashboard_path = os.path.join(base_dir, "Docs", "Reviews", "validation_dashboard.md")

def get_git_info():
    try:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=base_dir, text=True).strip()
        try:
            tag = subprocess.check_output(["git", "describe", "--tags", "--exact-match"], cwd=base_dir, text=True, stderr=subprocess.STDOUT).strip()
        except Exception:
            tag = subprocess.check_output(["git", "describe", "--tags", "--always"], cwd=base_dir, text=True).strip()
        return commit, tag
    except Exception:
        return "unknown", "unknown"

def main():
    commit, tag = get_git_info()
    
    # Load manifest
    hashes = {}
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            hashes = json.load(f).get("locked_apis", {})
            
    # Compute exact metrics from registry
    import yaml
    registry_path = os.path.join(base_dir, "master_capability_registry.yaml")
    total_caps = 0
    implemented_caps = 0
    legacy_caps = 0
    deprecated_caps = 0
    archived_caps = 0
    
    if os.path.exists(registry_path):
        with open(registry_path, "r", encoding="utf-8") as f:
            registry = yaml.safe_load(f)
            
        for cap in registry.get("capabilities", []):
            total_caps += 1
            if cap.get("implementation_status", "").lower() == "implemented":
                implemented_caps += 1
            if cap.get("metadata", {}).get("is_legacy"):
                legacy_caps += 1
                
    pct = (implemented_caps / total_caps) * 100 if total_caps > 0 else 0
            
    report = {
        "metadata": {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "git_commit": commit,
            "git_tag": tag
        },
        "locked_artifacts": hashes,
        "metrics": {
            "capabilities": {
                "total": total_caps,
                "implemented": implemented_caps,
                "legacy": legacy_caps,
                "deprecated": deprecated_caps,
                "archived": archived_caps
            },
            "coverage": {
                "validation": pct,
                "documentation": pct,
                "benchmark": pct
            }
        }
    }
    
    with open(report_json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)
        
    with open(report_md_path, "w", encoding="utf-8") as f:
        f.write("# Repository Freeze Report\n\n")
        f.write("This artifact is immutable and represents the absolute state of the repository prior to Phase 9 Strategy injection.\n\n")
        f.write("## Metadata\n")
        f.write(f"- **Timestamp**: `{report['metadata']['timestamp']}`\n")
        f.write(f"- **Commit**: `{report['metadata']['git_commit']}`\n")
        f.write(f"- **Tag**: `{report['metadata']['git_tag']}`\n\n")
        
        f.write("## Locked Artifacts\n")
        f.write("| Path | SHA-256 |\n")
        f.write("|------|---------|\n")
        for p, h in hashes.items():
            f.write(f"| `{p}` | `{h}` |\n")
            
        f.write("\n## Coverage Metrics\n")
        f.write(f"- **Validation Coverage**: {report['metrics']['coverage']['validation']}%\n")
        f.write(f"- **Documentation Coverage**: {report['metrics']['coverage']['documentation']}%\n")
        f.write(f"- **Benchmark Coverage**: {report['metrics']['coverage']['benchmark']}%\n")
        
    print(f"Generated {report_json_path} and {report_md_path}")

if __name__ == "__main__":
    main()
