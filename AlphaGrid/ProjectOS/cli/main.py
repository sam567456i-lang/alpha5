import sys
import argparse
from ProjectOS.capability.matrix_generator import CapabilityMatrixGenerator

def main():
    parser = argparse.ArgumentParser(description="Project OS CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # capability-matrix command
    subparsers.add_parser("capability-matrix", help="Generate the Master Capability Matrix")
    
    subparsers.add_parser("integrity-gate", help="Run the mandatory repository integrity gate")
    subparsers.add_parser("switches", help="Generate the Universal Switch Registry")
    subparsers.add_parser("reports", help="Generate all Governance Reports")
    subparsers.add_parser("audit", help="Run full repository audit")
    subparsers.add_parser("validate", help="Validate repository normalization")
    subparsers.add_parser("certify", help="Certify repository against governance gates")
    subparsers.add_parser("doc-impact", help="Generate Documentation Impact Report")
    subparsers.add_parser("doc-audit", help="Run the strict Documentation Synchronization Audit")
    subparsers.add_parser("freeze", help="Generate freeze report")
    
    # Classify command
    classify_parser = subparsers.add_parser("classify", help="Run Legacy Component Preservation & Classification Workflow")
    classify_parser.add_argument("--component", type=str, required=True, help="Component ID to classify")
    classify_parser.add_argument("--action", type=str, choices=["retain", "reuse", "extend", "migrate", "deprecate", "remove"], required=True, help="Proposed classification action")
    
    args = parser.parse_args()
    repo_root = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid"
    
    if args.command == "capability-matrix":
        print("Generating Master Capability Matrix...")
        gen = CapabilityMatrixGenerator(repo_root)
        gen.generate_matrix()
        print("Done.")
    elif args.command == "integrity-gate":
        from ProjectOS.validator.integrity_checker import IntegrityChecker
        checker = IntegrityChecker(repo_root)
        if not checker.run_integrity_gate():
            sys.exit(1)
    elif args.command == "switches":
        from ProjectOS.registry.switch_generator import SwitchGenerator
        gen = SwitchGenerator(repo_root)
        gen.generate_registry()
    elif args.command == "reports":
        from ProjectOS.reporter.report_generator import ReportGenerator
        gen = ReportGenerator(repo_root)
        gen.generate_all_reports()
    elif args.command == "doc-impact":
        from ProjectOS.reports.doc_impact_report import generate_doc_impact_report
        generate_doc_impact_report(repo_root)
    elif args.command == "doc-audit":
        from ProjectOS.certification.documentation_auditor import DocumentationAuditor
        auditor = DocumentationAuditor(repo_root)
        if not auditor.audit():
            sys.exit(1)
    elif args.command == "freeze":
        print("Initiating Repository Freeze Sequence...")
        from ProjectOS.certification.documentation_auditor import DocumentationAuditor
        auditor = DocumentationAuditor(repo_root)
        if not auditor.audit():
            print("\n[FREEZE ABORTED] You cannot freeze the repository while documentation is out of sync.")
            sys.exit(1)
        print("Documentation synced. Proceeding with freeze...")
    elif args.command == "classify":
        print("=========================================")
        print("Legacy Component Classification Report")
        print("=========================================")
        print(f"Component ID       : {args.component}")
        print(f"Proposed Action    : {args.action.upper()}")
        print("Classification Confidence: [Pending Scan]")
        print("-----------------------------------------")
        print("Evidence:")
        print("  - Repository Path: [Pending Scan]")
        print("  - Registry ID    : [Pending Scan]")
        print("  - Capability ID  : [Pending Scan]")
        print("  - Platform       : [Pending Scan]")
        print("  - Reason         : [Pending Scan]")
        print("  - Dependencies   : [Pending Scan]")
        print("  - Risk           : [Pending Scan]")
        print("-----------------------------------------")
        print("Impact Analysis:")
        print("  - Affected Platforms    : [Pending Scan]")
        print("  - Affected DTOs         : [Pending Scan]")
        print("  - Affected Registries   : [Pending Scan]")
        print("  - Affected Tests        : [Pending Scan]")
        print("  - Affected Documentation: [Pending Scan]")
        print("  - Affected Dashboards   : [Pending Scan]")
        print("  - Affected AI           : [Pending Scan]")
        print("  - Affected Methodologies: [Pending Scan]")
        print("  - Affected Plugins      : [Pending Scan]")
        print("-----------------------------------------")
        print("Risk Level         : High (Manual review mandatory)")
        print("\n[HUMAN APPROVAL REQUIRED] Please review the above classification evidence before proceeding with any implementation modifications.")
        print("To approve, record this classification into the architecture decision log.")
    else:
        print(f"Command '{args.command}' is scaffolded but not yet fully implemented in Project OS.")

if __name__ == "__main__":
    main()
