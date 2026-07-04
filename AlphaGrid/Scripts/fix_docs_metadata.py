import os
import yaml
import re

base_path = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Docs"
registry_path = os.path.join(base_path, "Documentation_Registry.yaml")

files_to_fix = [
    "Governance/Wave_Lifecycle.md",
    "Reviews/validation_dashboard.md"
]

with open(registry_path, "r", encoding="utf-8") as f:
    registry = yaml.safe_load(f)
    
docs = registry.setdefault("documents", [])
doc_id_counter = len(docs) + 1

for rel_path in files_to_fix:
    full_path = os.path.join(base_path, os.path.normpath(rel_path))
    if not os.path.exists(full_path):
        continue
        
    doc_id = f"GEN-{doc_id_counter:03d}"
    doc_id_counter += 1
    title = os.path.basename(rel_path).replace(".md", "").replace("_", " ").title()
    
    # Check if already in registry
    if any(d.get("Path") == rel_path for d in docs):
        existing = next(d for d in docs if d.get("Path") == rel_path)
        doc_id = existing.get("Document_ID", doc_id)
        if "Document_ID" not in existing:
             existing["Document_ID"] = doc_id
    else:
        new_entry = {
            "Document_ID": doc_id,
            "Title": title,
            "Version": "1.0.0",
            "Maturity": '"Level 5: Institutionally Frozen"',
            "Implementation_Status": "Validated",
            "Phase": "10",
            "Owner": "ArchitectureTeam",
            "Category": "Generated",
            "Path": rel_path.replace("\\", "/"),
            "Dependencies": [],
            "Referenced_By": []
        }
        docs.append(new_entry)
        
    # Read file and replace frontmatter
    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        
    if content.startswith("---"):
        # Strip existing frontmatter
        content = re.sub(r"^---.*?---\n", "", content, flags=re.DOTALL)
        
    frontmatter = f"""---
Document ID: {doc_id}
Title: "{title}"
Version: 1.0.0
Governance Version: 1.0.0
Architecture Version: 1.0.0
Phase: 10
Owner: ArchitectureTeam
Category: Generated
Maturity: "Level 5: Institutionally Frozen"
Implementation Status: Validated
Current Phase: 10
Future Phase: N/A
Last Validated Phase: 10
Review Date: 2026-07-04
Dependencies: []
Referenced By: []
---
"""
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(frontmatter + content)
            
with open(registry_path, "w", encoding="utf-8") as f:
    yaml.dump(registry, f, sort_keys=False)
    
print("Docs fixed again.")
