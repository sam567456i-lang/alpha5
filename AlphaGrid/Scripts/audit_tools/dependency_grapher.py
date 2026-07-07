import os
import ast
from pathlib import Path

def get_imports(filepath):
    imports = set()
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.add(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.add(node.module)
    except Exception as e:
        pass
    return imports

def build_graph(backend_dir):
    graph = {}
    for root, _, files in os.walk(backend_dir):
        if "archive" in root or "__pycache__" in root:
            continue
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                rel_path = os.path.relpath(path, backend_dir).replace(os.sep, ".")[:-3]
                graph[rel_path] = get_imports(path)
    return graph

def find_cycles(graph):
    visited = set()
    path = []
    cycles = []

    def visit(node):
        if node in path:
            cycle = path[path.index(node):] + [node]
            cycles.append(cycle)
            return
        if node in visited:
            return
        visited.add(node)
        path.append(node)
        for neighbor in graph.get(node, []):
            visit(neighbor)
        path.pop()

    for node in graph:
        visit(node)
    return cycles

if __name__ == "__main__":
    backend_dir = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Backend"
    print("Building Structural Dependency Graph...")
    graph = build_graph(backend_dir)
    print(f"Mapped {len(graph)} modules.")
    
    print("\nExecuting Circular Dependency Detection...")
    cycles = find_cycles(graph)
    if not cycles:
        print("PASS: No circular dependencies detected.")
    else:
        print(f"FAIL: Found {len(cycles)} circular dependencies.")
        for c in cycles:
            print(" -> ".join(c))
