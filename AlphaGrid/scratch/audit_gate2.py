import ast
import os

def audit_gate2():
    print("=== GATE 2: CROSS-PLATFORM CONTRACT AUDIT ===")
    
    repo_root = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid"
    
    # 1. Audit BaseEvent (P1-P4 boundary)
    events_path = os.path.join(repo_root, "Backend", "core", "events.py")
    passed_event = False
    with open(events_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == "BaseEvent":
                for child in node.body:
                    if isinstance(child, ast.AnnAssign) and child.target.id == "lineage":
                        if "Optional" in ast.unparse(child.annotation) and "LineageDTO" in ast.unparse(child.annotation):
                            passed_event = True

    print(f"BaseEvent LineageDTO Validation: {'PASS' if passed_event else 'FAIL'}")

    # 2. Audit BaseState (P5-P8 boundary)
    states_path = os.path.join(repo_root, "Backend", "core", "state.py")
    passed_state = False
    with open(states_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == "BaseState":
                for child in node.body:
                    if isinstance(child, ast.AnnAssign) and child.target.id == "lineage":
                        if "Optional" in ast.unparse(child.annotation) and "LineageDTO" in ast.unparse(child.annotation):
                            passed_state = True

    print(f"BaseState LineageDTO Validation: {'PASS' if passed_state else 'FAIL'}")

    # 3. Audit P8 Dependency Resolution (Registry-driven)
    plugin_fw_path = os.path.join(repo_root, "Backend", "platforms", "platform8_analysis", "plugin_framework.py")
    passed_registry = False
    with open(plugin_fw_path, "r", encoding="utf-8") as f:
        content = f.read()
        if "yaml.safe_load" in content and "registry_path" in content:
            passed_registry = True

    print(f"P8 Registry-Driven Validation: {'PASS' if passed_registry else 'FAIL'}")

    if passed_event and passed_state and passed_registry:
        print("GATE 2 PASSED: Foundational platforms structurally retrofitted.")
    else:
        print("GATE 2 FAILED: Missing architectural requirements in P0-P8.")

if __name__ == "__main__":
    audit_gate2()
