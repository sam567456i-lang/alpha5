"""Project OS CLI Entry Point"""
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description="AlphaGrid Project OS CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Verify command
    verify_parser = subparsers.add_parser("verify", help="Verify a phase's governance status")
    verify_parser.add_argument("--phase", required=True, help="Target phase (e.g., Platform11)")
    
    # Phase Exit command
    phase_exit_parser = subparsers.add_parser("phase-exit", help="Execute the Phase Exit Governance Pipeline")
    phase_exit_parser.add_argument("--phase", required=True, help="Target phase to freeze (e.g., Platform11)")
    
    args = parser.parse_args()
    
    if args.command == "verify":
        print(f"Project OS Verify: Checking phase {args.phase}")
        from ProjectOS.cli.verify import execute_verify
        execute_verify(args.phase)
    elif args.command == "phase-exit":
        print(f"Project OS Phase Exit: Initializing for {args.phase}")
        from ProjectOS.cli.phase_exit import execute_phase_exit
        execute_phase_exit(args.phase)
    else:
        parser.print_help()

if __name__ == "__main__":
    sys.exit(main())
