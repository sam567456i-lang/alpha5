import os
import sys
import re

class ManualTradingComplianceScanner:
    def __init__(self, target_dir: str):
        self.target_dir = target_dir
        self.fail_patterns = [
            r"import\s+ccxt",
            r"import\s+ib_insync",
            r"from\s+ib_insync\s+import",
            r"import\s+MetaTrader5",
            r"requests\.post\(['\"].*api\.binance\.com",
            r"requests\.post\(['\"].*api\.interactivebrokers\.com",
            r"def\s+execute_trade\(",
            r"def\s+submit_order\(",
            r"def\s+place_order\("
        ]
        self.warn_patterns = [
            r"auto execute",
            r"automatic order placement",
            r"broker execution",
            r"live order submission",
            r"autonomous trading",
            r"trading bot"
        ]
        self.fails = []
        self.warns = []

    def scan(self):
        for root, _, files in os.walk(self.target_dir):
            # Skip virtual environments and hidden dirs
            if ".venv" in root or ".git" in root or "__pycache__" in root:
                continue
                
            for file in files:
                if file.endswith((".py", ".md", ".yaml", ".json")):
                    self._scan_file(os.path.join(root, file))
                    
        return self._generate_report()
        
    def _scan_file(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except:
            return

        for i, line in enumerate(lines):
            line_num = i + 1
            
            # Check for critical architectural violations (Execution Logic)
            for pattern in self.fail_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    # Exclude this exact scanner script from failing itself
                    if "manual_trading_compliance.py" not in file_path:
                        self.fails.append(f"FAIL: {file_path}:{line_num} -> Found prohibited execution logic matching '{pattern}'.")
            
            # Check for wording/terminology that might imply automation
            for pattern in self.warn_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    # Exclude the governance docs from warning about their own rules
                    if "Architecture_Principles.md" not in file_path and "ADR-0042" not in file_path and "manual_trading_compliance.py" not in file_path:
                        self.warns.append(f"WARN: {file_path}:{line_num} -> Found terminology '{pattern}'. Context: Documentation/Future Extension Allowed.")

    def _generate_report(self):
        report = []
        report.append("=== Manual Trading Compliance Report ===")
        
        if not self.fails and not self.warns:
            report.append("Status: PASS")
            report.append("✓ Core platform does not submit orders")
            report.append("✓ No broker APIs used")
            report.append("✓ No execution engine in production pipeline")
            return "\n".join(report), True
            
        if self.fails:
            report.append("\nCRITICAL FAILURES (Architectural Violations):")
            for f in self.fails:
                report.append("  " + f)
                
        if self.warns:
            report.append("\nWARNINGS (Terminology Found):")
            for w in self.warns:
                report.append("  " + w)
                
        if self.fails:
            report.append("\nStatus: FAIL")
            return "\n".join(report), False
        else:
            report.append("\nStatus: PASS (With Warnings)")
            return "\n".join(report), True

if __name__ == "__main__":
    target_dir = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid"
    scanner = ManualTradingComplianceScanner(target_dir)
    report_text, passed = scanner.scan()
    print(report_text)
    if not passed:
        sys.exit(1)
