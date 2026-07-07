import os
import json
import ast

def scan_dependencies(root_dir):
    graph = {}
    
    for root, dirs, files in os.walk(root_dir):
        if ".git" in root or "__pycache__" in root or "venv" in root:
            continue
            
        for f in files:
            if f.endswith(".py"):
                filepath = os.path.join(root, f)
                relpath = os.path.relpath(filepath, root_dir)
                module_name = relpath.replace(os.sep, ".").replace(".py", "")
                
                imports = []
                try:
                    with open(filepath, "r", encoding="utf-8") as file:
                        tree = ast.parse(file.read())
                        for node in ast.walk(tree):
                            if isinstance(node, ast.Import):
                                for alias in node.names:
                                    imports.append(alias.name)
                            elif isinstance(node, ast.ImportFrom):
                                if node.module:
                                    imports.append(node.module)
                except Exception as e:
                    pass
                
                # Filter to internal dependencies only
                internal_imports = [imp for imp in imports if imp.startswith("Backend") or imp.startswith("Scripts") or imp.startswith("AlphaGrid")]
                graph[module_name] = internal_imports
                
    with open("dependency_graph.json", "w", encoding="utf-8") as f:
        json.dump(graph, f, indent=4)
        
    print(f"Dependency Scan Complete. Graph nodes: {len(graph)}.")

if __name__ == "__main__":
    scan_dependencies(r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid")
