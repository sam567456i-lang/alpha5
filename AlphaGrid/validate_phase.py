import argparse
import sys
import os
import json
import shutil
from datetime import datetime
from Backend.validation.dtos import ValidationContextDTO
from Backend.validation.validation_registry import ValidationRegistry
from Backend.validation.runner import ValidationRunner

def main():
    parser = argparse.ArgumentParser(description="AlphaGrid Phase Validation Engine")
    parser.add_argument("--phase", required=True, help="Target Phase (e.g. 10e)")
    parser.add_argument("--family", default="core", help="Target Family (e.g. momentum)")
    parser.add_argument("--profile", default="phase", help="Validation profile to run (quick, family, phase, release, production)")
    parser.add_argument("--dataset", default="default.parquet", help="Deterministic dataset to use")
    
    args = parser.parse_args()
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    registry_path = os.path.join(base_dir, "Docs", "Governance", "Validation_Registry.yaml")
    
    if not os.path.exists(registry_path):
        print(f"[FAIL] Validation Registry not found at {registry_path}")
        sys.exit(1)
        
    registry = ValidationRegistry(registry_path)
    runner = ValidationRunner(registry)
    
    evidence_dir = os.path.join(base_dir, "Docs", "Evidence", "2026", "EV-TEMP")
    os.makedirs(evidence_dir, exist_ok=True)
    
    # Generate Validation Manifest
    manifest = {
        "phase": args.phase,
        "family": args.family,
        "profile": args.profile,
        "dataset": args.dataset,
        "strategies": ["MACDMomentumStrategy", "ROCMomentumStrategy"] if args.family == "momentum" else [],
        "features": ["MACDFeatureGenerator", "ROCFeatureGenerator"] if args.family == "momentum" else [],
        "validators_executed": registry.resolve_profile(args.profile)
    }
    
    manifest_path = os.path.join(evidence_dir, "validation_manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=4)
    
    context = ValidationContextDTO(
        phase=args.phase,
        family=args.family if args.profile != "repository" else "ALL",
        git_commit="latest",
        registry_version="latest",
        dto_version="latest",
        config_version="latest",
        dataset=args.dataset,
        evidence_directory=evidence_dir,
        workspace=base_dir,
        profile=args.profile
    )
    
    print(f"=== AlphaGrid Validation Engine ===")
    print(f"Phase: {args.phase} | Family: {args.family} | Profile: {args.profile}\n")
    
    # --- Execute and Stream Events ---
    print(f"=== AlphaGrid Validation Engine ===")
    print(f"Phase: {args.phase} | Family: {args.family} | Profile: {args.profile}")
    print(f"Manifest: {manifest_path}\n")
    
    results = []
    all_passed = True
    
    try:
        for event in runner.execute(args.profile, context):
            if event.event_type == "VALIDATOR_FINISHED":
                r = event.result
                results.append(r)
                
                # Print beautiful progress row
                pct = event.progress_pct or 0.0
                bar = "=" * int(pct / 10) + "-" * (10 - int(pct / 10))
                
                dur = f"{r.duration_ms/1000.0:.2f} s"
                status_color = r.status # We could colorize, but plain text for now
                print(f"[{bar} {pct:>5.1f}%] {r.id:<32} {status_color:<8} ({dur})")
                
                if r.status not in ["PASS", "SKIPPED", "WARNING"]:
                    all_passed = False
                    
    except KeyboardInterrupt:
        print("\n[!] VALIDATION CANCELLED (Ctrl+C). Saving partial evidence...")
        all_passed = False
        # The runner handles marking current done, the rest aren't in results
        
    # --- Generate Validation Dashboard ---
    dashboard_path = os.path.join(base_dir, "Docs", "Reviews", "validation_dashboard.md")
    os.makedirs(os.path.dirname(dashboard_path), exist_ok=True)
    
    with open(dashboard_path, "w") as f:
        f.write(f"""---
Document ID: GEN-010
Title: "Validation Dashboard"
Version: 1.0.0
Governance Version: 1.0.0
Architecture Version: 1.0.0
Phase: 10
Owner: ArchitectureTeam
Category: Generated
Maturity: "Level 5: Institutionally Frozen"
Implementation Status: Validated
Current Phase: 10
Future Phase: N/A
Last Validated Phase: 10
Review Date: 2026-07-04
Dependencies: []
Referenced By: []
---

# Validation Dashboard (Phase {args.phase} - {args.family})\n\n""")
        f.write("| Validator | Status | Duration (ms) |\n")
        f.write("|-----------|--------|---------------|\n")
        for r in results:
            f.write(f"| {r.id} | **{r.status}** | {r.duration_ms:.1f} |\n")
        freeze_status = "ELIGIBLE" if all_passed else "BLOCKED"
        f.write(f"\n**Freeze Status**: {freeze_status}\n")
        
    # --- Append to Global History Index ---
    history_dir = os.path.join(base_dir, "Docs", "Validation", "history")
    os.makedirs(history_dir, exist_ok=True)
    history_path = os.path.join(history_dir, "validation_index.json")
    
    history_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "phase": args.phase,
        "family": args.family,
        "profile": args.profile,
        "duration_ms": sum(r.duration_ms for r in results) if results else 0,
        "status": "PASS" if all_passed else "FAIL",
        "evidence_id": os.path.basename(evidence_dir),
        "git_commit": "latest"
    }
    
    if args.phase == "10" and all_passed:
        ev_10i_path = os.path.join(os.path.dirname(evidence_dir), "EV-10I-A")
        if os.path.exists(ev_10i_path):
            shutil.rmtree(ev_10i_path)
        shutil.copytree(evidence_dir, ev_10i_path)
        print(f"Evidence officially archived to: {ev_10i_path}")
    
    history = []
    if os.path.exists(history_path):
        try:
            with open(history_path, "r") as f:
                history = json.load(f)
        except json.JSONDecodeError:
            pass
            
    history.append(history_entry)
    with open(history_path, "w") as f:
        json.dump(history, f, indent=4)
            
    # Summarize errors
    errors_found = [r for r in results if r.status in ["FAIL", "ERROR"]]
    if errors_found:
        print("\n=== FAILURE DETAILS ===")
        for r in errors_found:
            print(f"\n[{r.id}] - {r.status} ({r.reason})")
            print(f"Summary: {r.summary}")
            if r.errors:
                for e in r.errors:
                    print(f"  - {e}")
                    
    if all_passed:
        print(f"\n[CI SUCCESS] Validation profile '{args.profile}' completed successfully.")
        print(f"Evidence generated at: {evidence_dir}")
        print(f"Dashboard generated at: {dashboard_path}")
        sys.exit(0)
    else:
        print(f"\n[CI FAIL] Validation profile '{args.profile}' failed.")
        print(f"Evidence generated at: {evidence_dir}")
        sys.exit(1)

if __name__ == "__main__":
    main()
