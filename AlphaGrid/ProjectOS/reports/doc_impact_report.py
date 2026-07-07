import os
import json
from ProjectOS.certification.documentation_auditor import DocumentationAuditor

def generate_doc_impact_report(repo_root: str):
    auditor = DocumentationAuditor(repo_root)
    report = auditor.generate_impact_report()
    
    print("\n=============================================")
    print("      DOCUMENTATION IMPACT REPORT")
    print("=============================================\n")
    
    print(f"Status: {report['status']}")
    print("\nAffected Documents:")
    for doc in report.get("affected_documents", []):
        print(f"  - {doc}")
        
    if report.get("missing_updates"):
        print("\n[!] MISSING UPDATES (BLOCKING FREEZE):")
        for m in report["missing_updates"]:
            print(f"  - {m}")
            
    print("\n=============================================")
    
    # Save the report artifact
    reports_dir = os.path.join(repo_root, "Docs", "Reports")
    os.makedirs(reports_dir, exist_ok=True)
    report_path = os.path.join(reports_dir, "Doc_Impact_Report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"Report saved to {report_path}")
