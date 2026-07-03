import os
import yaml
import sys
import re
from pathlib import Path

base_path = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Docs"
registry_path = os.path.join(base_path, "Documentation_Registry.yaml")

errors = []

def error(msg):
    errors.append(msg)
    print(f"[FAIL] {msg}")

print("=== Starting Documentation CI Pipeline ===")

# Gate 1: Registry Validation
try:
    with open(registry_path, "r", encoding="utf-8") as f:
        registry = yaml.safe_load(f)
except Exception as e:
    error(f"Failed to parse Documentation_Registry.yaml: {e}")
    sys.exit(1)

reg_docs = registry.get("documents", [])
reg_ids = {}
reg_paths = {}

for d in reg_docs:
    doc_id = d.get("Document_ID")
    path = d.get("Path")
    
    if doc_id in reg_ids:
        error(f"Gate 3 (Duplicate): Duplicate Document ID in registry: {doc_id}")
    if not doc_id:
        error(f"Gate 1 (Metadata): Missing Document ID in registry entry: {d.get('Title')}")
        
    reg_ids[doc_id] = d
    if path:
        reg_paths[path] = d

# Gate 1 & 2: Metadata and Filesystem Consistency
fs_paths = set()
for root, _, files in os.walk(base_path):
    for f in files:
        if not f.endswith(".md"):
            continue
            
        filepath = os.path.join(root, f)
        rel_path = os.path.relpath(filepath, base_path).replace("\\", "/")
        fs_paths.add(rel_path)
        
        if rel_path not in reg_paths:
            error(f"Gate 2 (Registry): File exists on filesystem but not in registry: {rel_path}")
            
        with open(filepath, "r", encoding="utf-8", errors="ignore") as file_obj:
            content = file_obj.read()
            
        if not content.startswith("---"):
            error(f"Gate 1 (Metadata): Missing frontmatter in {rel_path}")
            continue
            
        try:
            fm_end = content.find("---", 3)
            fm_str = content[3:fm_end]
            fm = yaml.safe_load(fm_str)
            
            required_fields = ["Document ID", "Version", "Owner", "Category", "Phase", "Review Date", "Dependencies"]
            for field in required_fields:
                if field not in fm:
                    error(f"Gate 1 (Metadata): Missing required field '{field}' in {rel_path}")
                    
            if fm.get("Document ID") not in reg_ids:
                error(f"Gate 2 (Registry): Document ID {fm.get('Document ID')} from {rel_path} not found in registry")
                
            # Gate 4: Link Validation (basic internal markdown link check)
            links = re.findall(r"\[.*?\]\((?!http|mailto)(.*?)\)", content)
            for link in links:
                if link.startswith("#"): continue # anchor
                link_path = link.split("#")[0]
                target = os.path.normpath(os.path.join(root, link_path))
                if not os.path.exists(target):
                    error(f"Gate 4 (Links): Broken link in {rel_path} -> {link}")
                    
        except Exception as e:
            error(f"Gate 1 (Metadata): YAML parse error in {rel_path}: {e}")

for r_path in reg_paths:
    if r_path not in fs_paths:
        error(f"Gate 2 (Registry): Registry lists file that does not exist on filesystem: {r_path}")

if errors:
    print(f"\n[CI FAIL] {len(errors)} validation errors detected.")
    sys.exit(1)
else:
    print("\n[CI SUCCESS] All documentation validation gates passed.")
    sys.exit(0)
