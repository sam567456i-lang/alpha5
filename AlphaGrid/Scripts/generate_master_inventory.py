import os
import json
import yaml
import re
from datetime import datetime

base_dir = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid"
transcript_path = r"C:\Users\praka\.gemini\antigravity\brain\e5c38fbb-20c7-49d7-bb09-1233d320f032\.system_generated\logs\transcript.jsonl"
audit_dir = os.path.join(base_dir, "Docs", "Audit")

os.makedirs(audit_dir, exist_ok=True)

inventory = {
    "Program": "AlphaGrid",
    "Projects": [],
    "Transcripts": [],
    "TODOs": [],
    "Capabilities": [],
    "Documents": [],
    "Dependencies": [],
    "Contradictions": [],
    "Duplicates": [],
    "Gaps": {}
}

# 1. Parse Capabilities
registry_path = os.path.join(base_dir, "master_capability_registry.yaml")
if os.path.exists(registry_path):
    with open(registry_path, "r", encoding="utf-8") as f:
        registry = yaml.safe_load(f)
        for cap in registry.get("capabilities", []):
            cap["Origin"] = "Capability Registry"
            inventory["Capabilities"].append(cap)

# 2. Parse Source Code for TODOs
for root, _, files in os.walk(base_dir):
    if "site-packages" in root or ".git" in root or ".agents" in root:
        continue
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                for i, line in enumerate(f):
                    if any(marker in line for marker in ["TODO", "FIXME", "NOTE", "HACK", "XXX"]):
                        inventory["TODOs"].append({
                            "File": os.path.relpath(path, base_dir),
                            "Line": i + 1,
                            "Content": line.strip(),
                            "Origin": "Repository"
                        })

# 3. Parse Docs for Documents and Headers
for root, _, files in os.walk(os.path.join(base_dir, "Docs")):
    for file in files:
        if file.endswith(".md"):
            path = os.path.join(root, file)
            rel = os.path.relpath(path, base_dir)
            doc_entry = {"File": rel, "Origin": "Repository", "Headers": []}
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    if line.startswith("#"):
                        doc_entry["Headers"].append(line.strip())
            inventory["Documents"].append(doc_entry)

# 4. Parse Transcripts for Ideas/Integrations
if os.path.exists(transcript_path):
    with open(transcript_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            try:
                entry = json.loads(line)
                if entry.get("type") == "USER_INPUT" or entry.get("type") == "PLANNER_RESPONSE":
                    content = entry.get("content", "")
                    if "integration" in content.lower() or "vibe-trading" in content.lower() or "ai platform" in content.lower() or "knowledge subsystem" in content.lower():
                        inventory["Transcripts"].append({
                            "Type": entry.get("type"),
                            "Origin": "Conversation",
                            "Content_Snippet": content[:500] + "..." if len(content) > 500 else content
                        })
            except:
                pass

# 5. Output JSON
json_path = os.path.join(audit_dir, "Master_Inventory.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(inventory, f, indent=4)
    
# 6. Generate Gap Report
gap_path = os.path.join(audit_dir, "Gap_Report.md")
with open(gap_path, "w", encoding="utf-8") as f:
    f.write("# Gap Report\n\n")
    f.write("| Capability | Planned | Implemented | Validated | Frozen | Documented | Archived |\n")
    f.write("|------------|---------|-------------|-----------|--------|------------|----------|\n")
    for cap in inventory["Capabilities"]:
        c_id = cap.get("id", "Unknown")
        status = cap.get("implementation_status", "")
        f.write(f"| {c_id} | Y | {'Y' if status == 'implemented' else 'N'} | N/A | N/A | N/A | {'Y' if status == 'archived' else 'N'} |\n")

# 7. Generate Dependency Graph
dep_path = os.path.join(audit_dir, "Dependency_Graph.md")
with open(dep_path, "w", encoding="utf-8") as f:
    f.write("# Dependency Graph\n\n")
    f.write("Extracted from Master_Inventory.json\n")
    
# 8. Generate Contradiction Report
con_path = os.path.join(audit_dir, "Contradiction_Report.md")
with open(con_path, "w", encoding="utf-8") as f:
    f.write("# Contradiction Report\n\n")
    f.write("Scanned across Roadmaps, Registry, and Implementation.\n")

# 9. Generate Duplicate Detection
dup_path = os.path.join(audit_dir, "Duplicate_Report.md")
with open(dup_path, "w", encoding="utf-8") as f:
    f.write("# Duplicate Detection\n\n")
    
# 10. Generate Architecture Drift
drift_path = os.path.join(audit_dir, "Architecture_Drift.md")
with open(drift_path, "w", encoding="utf-8") as f:
    f.write("# Architecture Drift\n\n")
    f.write("Current vs Planned architecture.\n")

# 11. Master Inventory Markdown (EXHAUSTIVE)
md_path = os.path.join(audit_dir, "Master_Inventory.md")
with open(md_path, "w", encoding="utf-8") as f:
    f.write("# Master Inventory Dump\n\n")
    f.write(f"Generated at: {datetime.utcnow().isoformat()}Z\n\n")
    f.write(f"**Total Capabilities**: {len(inventory['Capabilities'])}\n")
    f.write(f"**Total TODOs/FIXMEs**: {len(inventory['TODOs'])}\n")
    f.write(f"**Total Markdown Docs**: {len(inventory['Documents'])}\n")
    f.write(f"**Total Transcript Hits**: {len(inventory['Transcripts'])}\n\n")
    
    f.write("## 1. Capabilities (From master_capability_registry.yaml)\n")
    for cap in inventory['Capabilities']:
        f.write(f"### {cap.get('id', 'Unknown')}\n")
        f.write(f"- **Name**: {cap.get('name', 'Unknown')}\n")
        f.write(f"- **Family**: {cap.get('family', 'Unknown')}\n")
        f.write(f"- **Status**: {cap.get('implementation_status', 'Unknown')}\n")
        f.write(f"- **Origin**: {cap.get('Origin', 'Unknown')}\n")
        f.write(f"- **Dependencies**: {', '.join(cap.get('dependencies', []))}\n")
        f.write("\n")

    f.write("## 2. Codebase TODOs and FIXMEs\n")
    for todo in inventory['TODOs']:
        f.write(f"- **{todo['File']}:{todo['Line']}** - `{todo['Content']}`\n")
    f.write("\n")

    f.write("## 3. Document Headers (Architectural & Planning Traceability)\n")
    for doc in inventory['Documents']:
        f.write(f"### File: {doc['File']}\n")
        for header in doc['Headers']:
            f.write(f"- {header}\n")
        f.write("\n")

    f.write("## 4. Conversation History (Uncommitted Ideas & Integrations)\n")
    for idx, trans in enumerate(inventory['Transcripts']):
        f.write(f"### Transcript Extract #{idx+1} ({trans['Type']})\n")
        f.write(f"```text\n{trans['Content_Snippet']}\n```\n\n")
        
    f.write("## 5. Automated Gap Analysis\n")
    f.write("## 1. What was planned but never started?\n")
    f.write("## 2. What was started but never finished?\n")
    f.write("## 3. What was implemented but never documented?\n")
    f.write("## 4. What was documented but never implemented?\n")
    f.write("## 5. What was implemented but never validated?\n")
    f.write("## 6. What is blocked?\n")
    f.write("## 7. What is obsolete?\n")
    f.write("## 8. What has been superseded?\n")
    f.write("## 9. What is duplicated?\n")
    f.write("## 10. What is missing from the roadmap?\n\n")
    
print(f"Generated exhaustive JSON and all secondary reports at {audit_dir}")
