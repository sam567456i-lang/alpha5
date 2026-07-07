import os
import subprocess
import datetime
from pathlib import Path

def generate_report():
    backend_root = Path(__file__).resolve().parent.parent.parent
    report_path = backend_root / "Platform10_Freeze_Report.md"
    tests_path = backend_root / "tests"
    
    cert_test = tests_path / "test_platform10_certification.py"
    purity_test = tests_path / "test_platform10_purity.py"
    
    try:
        cert_res = subprocess.run(["python", "-m", "pytest", str(cert_test)], capture_output=True, text=True, cwd=str(backend_root))
        purity_res = subprocess.run(["python", "-m", "pytest", str(purity_test)], capture_output=True, text=True, cwd=str(backend_root))
        
        cert_pass = cert_res.returncode == 0
        purity_pass = purity_res.returncode == 0
    except Exception as e:
        cert_pass = False
        purity_pass = False
        cert_res = f"Error: {e}"
        purity_res = ""

    overall_status = "FROZEN" if cert_pass and purity_pass else "FAIL"

    report_content = f"""# Platform 10 Freeze Report
Generated: {datetime.datetime.now().isoformat()}

## Overall Status: **{overall_status}**

### Component Certification
- Certification Tests: {'PASS' if cert_pass else 'FAIL'}
- Purity Tests: {'PASS' if purity_pass else 'FAIL'}

### Details

#### Certification Tests Output
```
{cert_res.stdout if hasattr(cert_res, 'stdout') else cert_res}
```

#### Purity Tests Output
```
{purity_res.stdout if hasattr(purity_res, 'stdout') else purity_res}
```
"""
    
    with open(report_path, "w") as f:
        f.write(report_content)
        
    print(f"Report generated at {report_path} with status {overall_status}")

if __name__ == "__main__":
    generate_report()
