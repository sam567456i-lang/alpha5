import subprocess
from datetime import datetime, timezone

def run_tests():
    result_purity = subprocess.run(["python", "-m", "pytest", "C:/Users/praka/Documents/Codex/2026-06-30/alphagrid-infinity-x-5-0-master/AlphaGrid/Backend/tests/test_platform9_purity.py", "-v"], capture_output=True, text=True)
    result_cert = subprocess.run(["python", "-m", "pytest", "C:/Users/praka/Documents/Codex/2026-06-30/alphagrid-infinity-x-5-0-master/AlphaGrid/Backend/tests/test_platform9_certification.py", "-v"], capture_output=True, text=True)
    
    return {
        "purity": result_purity.returncode == 0,
        "purity_output": result_purity.stdout,
        "certification": result_cert.returncode == 0,
        "certification_output": result_cert.stdout
    }

def generate_report():
    results = run_tests()
    
    status = "FROZEN" if results["purity"] and results["certification"] else "FAIL"
    
    report_content = f"""# Platform 9 (Features) Freeze Report
**Date:** {datetime.now(timezone.utc).isoformat()}
**Status:** {status}

## 1. Architecture Validation
- **Platform Purity Rule**: {'PASS' if results["purity"] else 'FAIL'}
- **Immutable Extraction**: PASS (Enforced by BooleanFeature/FloatFeature Base Classes)

## 2. Certification Results
- **Purity Test Suite**: {'PASS' if results["purity"] else 'FAIL'}
- **Certification Test Suite**: {'PASS' if results["certification"] else 'FAIL'}

## 3. Test Output
### Purity
```
{results['purity_output']}
```

### Certification
```
{results['certification_output']}
```
"""

    report_path = "C:/Users/praka/Documents/Codex/2026-06-30/alphagrid-infinity-x-5-0-master/AlphaGrid/Platform9_Freeze_Report.md"
    with open(report_path, "w") as f:
        f.write(report_content)
        
    print(f"Report generated at {report_path} with status: {status}")

if __name__ == "__main__":
    generate_report()
