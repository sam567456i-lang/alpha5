import yaml
import sys
from collections import defaultdict

REGISTRY_PATH = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Docs\Governance\registry\analytical_rule_registry.yaml"

def audit_registry():
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    rules = data.get("rules", [])
    rule_map = {r["id"]: r for r in rules}
    
    errors = []

    # 1. Duplicate IDs
    seen = set()
    for r in rules:
        if r["id"] in seen:
            errors.append(f"Duplicate Rule ID: {r['id']}")
        seen.add(r["id"])

    # 2. Dependency Tier Violations & Missing Dependencies
    for r in rules:
        tier = r.get("tier", 0)
        for dep in r.get("dependencies", []):
            if dep not in rule_map:
                errors.append(f"Rule {r['id']} depends on missing rule {dep}")
                continue
            
            dep_tier = rule_map[dep].get("tier", 0)
            if dep_tier >= tier and tier != 0:
                errors.append(f"Tier Violation: Rule {r['id']} (Tier {tier}) depends on {dep} (Tier {dep_tier})")

    # 3. Cycle Detection
    visited = set()
    path = set()
    
    def dfs(node):
        if node in path:
            errors.append(f"Cycle detected involving Rule {node}")
            return True
        if node in visited:
            return False
            
        visited.add(node)
        path.add(node)
        
        for dep in rule_map.get(node, {}).get("dependencies", []):
            if dfs(dep):
                return True
                
        path.remove(node)
        return False

    for r in rules:
        dfs(r["id"])

    if errors:
        print("Rule Dependency Audit FAILED:")
        for e in errors:
            print(f" - {e}")
        sys.exit(1)
    else:
        print("Rule Dependency Audit PASSED. No tier violations or cycles found.")

if __name__ == "__main__":
    audit_registry()
