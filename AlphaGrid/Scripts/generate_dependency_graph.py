import os
import yaml

base_dir = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid"
registry_path = os.path.join(base_dir, "master_capability_registry.yaml")
graph_path = os.path.join(base_dir, "Docs", "Architecture", "capability_dependency_graph.md")

with open(registry_path, "r", encoding="utf-8") as f:
    registry = yaml.safe_load(f)

capabilities = {cap["name"]: cap for cap in registry.get("capabilities", [])}

# Find all strategies
strategies = [cap for cap in registry.get("capabilities", []) if cap.get("owner_layer") == "Strategy"]

def trace_dependencies(cap_name, depth=0):
    indent = "  " * depth
    out = f"{indent}- {cap_name}\n"
    
    cap = capabilities.get(cap_name)
    if not cap:
        return out
        
    deps = cap.get("depends_on", [])
    if not isinstance(deps, list):
        deps = [deps]
        
    for dep in deps:
        if dep:
            out += trace_dependencies(dep, depth + 1)
            
    return out

with open(graph_path, "w", encoding="utf-8") as f:
    f.write("# Capability Dependency Graph\n\n")
    f.write("Generated from `master_capability_registry.yaml`\n\n")
    
    if not strategies:
        # Fallback for now if no strategies are explicitly named Strategy in registry
        strategies = [cap for cap in registry.get("capabilities", []) if cap.get("owner_layer") == "Methodology"]
        
    for strategy in strategies:
        f.write(trace_dependencies(strategy["name"]))
        f.write("\n")
        
print(f"Dependency graph written to {graph_path}")
