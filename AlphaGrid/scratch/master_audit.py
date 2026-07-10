import os
import ast
import json
import re

def analyze_directory(root_dir):
    inventory = []
    placeholders = []
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if any(ignored in dirpath for ignored in [".git", "__pycache__", "venv", ".pytest_cache", ".ruff_cache", ".mypy_cache"]):
            continue
            
        for file in filenames:
            if not file.endswith(".py"):
                continue
                
            filepath = os.path.join(dirpath, file)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Check for placeholders
            for i, line in enumerate(content.split("\n")):
                if re.search(r'\b(pass|TODO|FIXME|NotImplemented|NotImplementedError|Stub|Mock)\b', line, re.IGNORECASE):
                    placeholders.append({
                        "file": filepath,
                        "line": i + 1,
                        "content": line.strip()
                    })
                    
            try:
                tree = ast.parse(content)
                classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
                functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
                
                inventory.append({
                    "file": filepath,
                    "classes": classes,
                    "functions": functions
                })
            except SyntaxError:
                pass
                
    return {"inventory": inventory, "placeholders": placeholders}

if __name__ == "__main__":
    report = analyze_directory("Backend")
    with open("master_audit_raw.json", "w") as f:
        json.dump(report, f, indent=2)
    print(f"Scanned {len(report['inventory'])} Python files. Found {len(report['placeholders'])} placeholders.")
