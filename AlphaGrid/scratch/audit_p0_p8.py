import os
import ast

def find_dtos_without_lineage(repo_root: str):
    p0_p8_dirs = [
        "config",
        "data",
        "market_data",
        "math",
        "indicator_engine",
        "market_foundation",
        "market_intelligence",
        "analytics",
        os.path.join("platforms", "platform8_analysis")
    ]
    
    backend_dir = os.path.join(repo_root, "Backend")
    
    results = []
    
    for pd in p0_p8_dirs:
        full_dir = os.path.join(backend_dir, pd)
        if not os.path.exists(full_dir):
            continue
            
        for root, dirs, files in os.walk(full_dir):
            for file in files:
                if file.endswith(".py"):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, "r", encoding="utf-8") as f:
                            content = f.read()
                        
                        tree = ast.parse(content)
                        for node in ast.walk(tree):
                            if isinstance(node, ast.ClassDef):
                                if "DTO" in node.name:
                                    # Check base classes
                                    bases = [b.id for b in node.bases if isinstance(b, ast.Name)]
                                    if "LineageDTO" not in bases:
                                        # Now, remember user rule: "Level 2 — Platform Boundary DTOs (Mandatory lineage) ... Level 1 — Internal Working DTOs (No mandatory lineage)".
                                        # Let's flag all of them for review.
                                        results.append(f"{pd} -> {file} -> {node.name} (Bases: {bases})")
                    except Exception as e:
                        print(f"Error parsing {filepath}: {e}")
                        
    return results

if __name__ == "__main__":
    res = find_dtos_without_lineage(r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid")
    for r in res:
        print(r)
