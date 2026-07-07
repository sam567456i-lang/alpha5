import os
import json
import ast

def scan_inventory(root_dir):
    inventory = {
        "directories": 0,
        "files": 0,
        "python_modules": [],
        "yaml_configs": [],
        "markdown_docs": [],
        "classes": [],
        "functions": [],
        "other_files": []
    }
    
    for root, dirs, files in os.walk(root_dir):
        if ".git" in root or "__pycache__" in root or "venv" in root:
            continue
            
        inventory["directories"] += 1
        for f in files:
            inventory["files"] += 1
            filepath = os.path.join(root, f)
            relpath = os.path.relpath(filepath, root_dir)
            
            if f.endswith(".py"):
                inventory["python_modules"].append(relpath)
                try:
                    with open(filepath, "r", encoding="utf-8") as file:
                        tree = ast.parse(file.read())
                        for node in ast.walk(tree):
                            if isinstance(node, ast.ClassDef):
                                inventory["classes"].append({"name": node.name, "file": relpath})
                            elif isinstance(node, ast.FunctionDef):
                                inventory["functions"].append({"name": node.name, "file": relpath})
                except Exception as e:
                    pass
            elif f.endswith(".yaml") or f.endswith(".yml"):
                inventory["yaml_configs"].append(relpath)
            elif f.endswith(".md"):
                inventory["markdown_docs"].append(relpath)
            else:
                inventory["other_files"].append(relpath)
                
    with open("inventory_report.json", "w", encoding="utf-8") as f:
        json.dump(inventory, f, indent=4)
        
    print(f"Inventory Complete: {inventory['files']} files, {len(inventory['classes'])} classes, {len(inventory['functions'])} functions.")

if __name__ == "__main__":
    scan_inventory(r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid")
