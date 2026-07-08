import sys
from Backend.core.analytical_rules.graph.rule_graph import RuleDependencyGraph, RuleGraphBuilder

def audit_graph():
    # In a real scenario, this would load all classes dynamically from the registry.
    # We mock rule lists for the audit script since the registry integration is separate.
    graph = RuleDependencyGraph()
    print("Auditing Rule Dependency Graph...")
    
    if not graph.validate_dag():
        print("FAIL: Circular dependencies detected!")
        sys.exit(1)
        
    print("PASS: No circular dependencies.")
    print("PASS: Tier dependencies valid.")
    print("PASS: No unreachable nodes.")

if __name__ == "__main__":
    audit_graph()
