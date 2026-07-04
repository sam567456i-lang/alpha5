import os
import json
import time
from Backend.validation.dtos import ValidationContextDTO
from Backend.validation.validators.legacy_equivalence_validator import LegacyEquivalenceValidator
from Backend.validation.validators.dependency_validator import DependencyValidator
from Backend.validation.validators.performance_validator import PerformanceValidator

def run_wave1_validation():
    workspace = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    context = ValidationContextDTO(
        phase="EV-10I-B-WAVE1",
        family="momentum",
        git_commit="latest",
        registry_version="latest",
        dto_version="latest",
        config_version="latest",
        dataset="reference.parquet",
        evidence_directory=os.path.join(workspace, "Docs", "Evidence", "2026", "EV-10I-B-WAVE1"),
        workspace=workspace,
        profile="default"
    )
    
    validators = [
        LegacyEquivalenceValidator("VAL-LEGACY-EQ", "Verify numerical equivalence against legacy implementation"),
        DependencyValidator("VAL-DEP", "Verify Math Core dependency constraints"),
        PerformanceValidator("VAL-PERF", "Verify SLA latency constraints"),
    ]
    
    ev_dir = os.path.join(workspace, "Docs", "Evidence", "2026", "EV-10I-B-WAVE1")
    os.makedirs(ev_dir, exist_ok=True)
    
    results = []
    
    for validator in validators:
        print(f"Running {validator.validator_id}...")
        try:
            res = validator.run_validation(context)
            results.append({
                "id": res.id,
                "status": res.status,
                "duration_ms": res.duration_ms,
                "errors": res.errors,
                "summary": res.summary
            })
        except Exception as e:
            results.append({
                "id": validator.validator_id,
                "status": "ERROR",
                "duration_ms": 0.0,
                "errors": [str(e)],
                "summary": "Exception during execution"
            })
            
    with open(os.path.join(ev_dir, "validation_report.json"), "w") as f:
        json.dump(results, f, indent=4)
        
    with open(os.path.join(ev_dir, "validation_report.md"), "w") as f:
        f.write("# Phase 10i-B Wave 1 MACD Validation Report\n\n")
        for r in results:
            f.write(f"## {r['id']} - {r['status']}\n")
            f.write(f"- Duration: {r['duration_ms']:.2f}ms\n")
            f.write(f"- Summary: {r['summary']}\n")
            if r['errors']:
                f.write("- Errors:\n")
                for err in r['errors']:
                    f.write(f"  - {err}\n")
            f.write("\n")
            
    print("Validation completed. Results saved to Docs/Evidence/2026/EV-10I-B-WAVE1/")

if __name__ == "__main__":
    run_wave1_validation()
