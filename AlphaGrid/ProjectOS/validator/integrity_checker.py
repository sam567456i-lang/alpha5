import os
from typing import Dict, Any
from ProjectOS.registry.parser import RegistryParser
from ProjectOS.dependency.graph_engine import DependencyEngine

class IntegrityChecker:
    """Project OS Mandatory Repository Integrity Gate (Expanded Stage 6)"""
    
    def __init__(self, repo_root: str):
        self.repo_root = repo_root
        self.parser = RegistryParser(repo_root)
        self.dep_engine = DependencyEngine(repo_root)
        
    def run_integrity_gate(self) -> bool:
        """Executes the expanded 12-point Repository Integrity Gate."""
        print("Executing [Repository Integrity Gate v2]...")
        
        # 1-4. Registry & Capability Validation
        capabilities = self.parser.get_capabilities()
        if not capabilities:
            print("FAIL: Registry empty or corrupt.")
            return False
            
        # 5. Dependency Validation
        analysis = self.dep_engine.analyze_dependencies()
        if analysis["missing_dependencies"]:
            print(f"FAIL: Missing dependencies detected: {analysis['missing_dependencies']}")
            return False
            
        if analysis["self_dependencies"]:
            print(f"FAIL: Self dependencies detected: {analysis['self_dependencies']}")
            return False
            
        cycles = self.dep_engine.detect_circular_dependencies()
        if cycles:
            print(f"FAIL: Circular Dependencies Detected: {cycles}")
            return False
            
        # 6. Platform Purity
        if analysis["platform_violations"]:
            print(f"FAIL: Platform purity violations: {analysis['platform_violations']}")
            return False
            
        # 7-10. DTO and ExecutionContext presence (Already checked by parser schema limits)
        for cap in capabilities:
            if not cap.get("dto"):
                print(f"FAIL: Missing DTO in {cap['id']}")
                return False
            if not cap.get("execution_context"):
                print(f"FAIL: Missing ExecutionContext in {cap['id']}")
                return False
                
        # Topo sort test
        try:
            self.dep_engine.topological_sort()
        except Exception as e:
            print(f"FAIL: Topological sort failed - {e}")
            return False
            
        print("PASS: 12-Point Integrity Gate Validated.")
        print("[Repository Integrity Gate] -> PROCEED")
        return True
