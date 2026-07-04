import os
import sys
import yaml

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

def generate_capability_graph():
    docs_dir = os.path.join(project_root, "Docs", "Architecture")
    os.makedirs(docs_dir, exist_ok=True)
    out_path = os.path.join(docs_dir, "capability_dependency_graph.md")
    
    registry_path = os.path.join(project_root, "master_capability_registry.yaml")
    
    with open(registry_path, "r", encoding="utf-8") as f:
        registry = yaml.safe_load(f)
        
    capabilities = registry.get("capabilities", [])
    
    nodes_by_layer = {
        "Methodology": [],
        "Concept": [],
        "Feature": [],
        "Geometry": [],
        "Candlestick": [],
        "General": []
    }
    
    edges = []
    
    for cap in capabilities:
        layer = cap.get("owner_layer", cap.get("category", "General"))
        if layer not in nodes_by_layer:
            nodes_by_layer[layer] = []
            
        cap_id = cap["id"]
        name = cap["name"]
        nodes_by_layer[layer].append((cap_id, name))
        
        consumes = cap.get("consumes", [])
        for c in consumes:
            # We map consuming by name in the YAML, so we must find the id of the consumed capability
            consumed_id = next((x["id"] for x in capabilities if x["name"] == c), None)
            if consumed_id:
                edges.append((cap_id, consumed_id))
    
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("# Capability Dependency Graph\n\n")
        f.write("This document tracks the dependency graph of all capabilities across layers.\n\n")
        
        f.write("```mermaid\n")
        f.write("graph TD\n")
        
        # Write nodes grouped by layer
        for layer, nodes in nodes_by_layer.items():
            if not nodes:
                continue
            f.write(f"    %% {layer}\n")
            for cap_id, name in nodes:
                # Sanitize name for mermaid
                clean_name = name.replace("(", "").replace(")", "").replace('"', '')
                f.write(f"    {cap_id.replace('-', '_')}Label[\"{clean_name}\"]\n")
        
        f.write("\n    %% Edges\n")
        for cap_id, consumed_id in edges:
            f.write(f"    {cap_id.replace('-', '_')}Label --> {consumed_id.replace('-', '_')}Label\n")
            
        f.write("```\n")
        
    print(f"Successfully generated Capability Dependency Graph at {out_path}")

if __name__ == "__main__":
    generate_capability_graph()
