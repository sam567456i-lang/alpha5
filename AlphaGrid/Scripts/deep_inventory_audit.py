import os
import json
import yaml
import re
from datetime import datetime

base_dir = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid"
brain_dir = r"C:\Users\praka\.gemini\antigravity\brain"
audit_dir = os.path.join(base_dir, "Docs", "Audit")
os.makedirs(audit_dir, exist_ok=True)

inventory = {
    "Program": "AlphaGrid",
    "Phases": {},
    "Capabilities": {},
    "Validators": {},
    "ADRs": [],
    "TODOs": [],
    "Transcripts_Mentions": []
}

# 1. Parse Capabilities from YAML
registry_path = os.path.join(base_dir, "master_capability_registry.yaml")
if os.path.exists(registry_path):
    with open(registry_path, "r", encoding="utf-8") as f:
        registry = yaml.safe_load(f)
        for cap in registry.get("capabilities", []):
            cap_id = cap.get("id", "Unknown")
            inventory["Capabilities"][cap_id] = cap

# 2. Extract TODOs from ALL files
for root, _, files in os.walk(base_dir):
    if any(x in root for x in [".git", "site-packages", ".agents", "Docs"]):
        continue
    for file in files:
        if file.endswith((".py", ".json", ".yaml", ".yml", ".md", ".sh", ".ts", ".tsx")):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    for i, line in enumerate(f):
                        if any(marker in line for marker in ["TODO", "FIXME", "NOTE", "HACK", "XXX"]):
                            inventory["TODOs"].append({
                                "File": os.path.relpath(path, base_dir),
                                "Line": i + 1,
                                "Content": line.strip()
                            })
            except Exception:
                pass

# 3. Parse Roadmaps into Structured Tree
roadmap_dir = os.path.join(base_dir, "Docs", "Roadmaps")
if os.path.exists(roadmap_dir):
    for file in os.listdir(roadmap_dir):
        if file.endswith(".md"):
            with open(os.path.join(roadmap_dir, file), "r", encoding="utf-8", errors="ignore") as f:
                current_phase = None
                current_wave = None
                for line in f:
                    line = line.strip()
                    # Match Phase
                    phase_match = re.match(r"^##\s*(Phase\s*\d+.*)", line)
                    if not phase_match:
                        phase_match = re.match(r"^##\s*\d+\.\s*(.*Phase\s*\d+.*)", line)
                        if not phase_match:
                            phase_match = re.match(r"^##\s*\d+\.\s*([^:\n]+)", line)
                    
                    if phase_match:
                        current_phase = phase_match.group(1).strip()
                        if current_phase not in inventory["Phases"]:
                            inventory["Phases"][current_phase] = {}
                        current_wave = None
                        continue
                    
                    # Match Wave
                    wave_match = re.match(r"^\*\*(Wave\s*\d+.*)\*\*", line)
                    if wave_match and current_phase:
                        current_wave = wave_match.group(1).strip()
                        if current_wave not in inventory["Phases"][current_phase]:
                            inventory["Phases"][current_phase][current_wave] = []
                        continue
                        
                    # Match Capability / Task
                    task_match = re.match(r"^- \[([ xX])\] (.*)", line)
                    if task_match and current_phase:
                        status = "implemented" if task_match.group(1).lower() == "x" else "planned"
                        cap_name = task_match.group(2).strip()
                        
                        target_list = inventory["Phases"][current_phase].get(current_wave, []) if current_wave else inventory["Phases"][current_phase].setdefault("General", [])
                        target_list.append({
                            "Name": cap_name,
                            "Status": status,
                            "Source": file
                        })
                        if current_wave:
                            inventory["Phases"][current_phase][current_wave] = target_list

# 4. Generate JSON
with open(os.path.join(audit_dir, "Master_Inventory.json"), "w", encoding="utf-8") as f:
    json.dump(inventory, f, indent=4)

# 5. Gap Report
gap_md = "# Gap Report\n\n| Capability | Roadmap Status | Registry Status | Gap Detected |\n|---|---|---|---|\n"
capabilities_in_roadmap = {}
for phase, waves in inventory["Phases"].items():
    for wave, caps in waves.items():
        for cap in caps:
            name = cap["Name"]
            capabilities_in_roadmap[name] = cap["Status"]

registry_names = {v.get("name", ""): v.get("implementation_status", "unknown") for k, v in inventory["Capabilities"].items()}

for rm_name, rm_status in capabilities_in_roadmap.items():
    reg_status = registry_names.get(rm_name, "Missing from Registry")
    gap = "YES" if reg_status == "Missing from Registry" or rm_status != reg_status else "NO"
    gap_md += f"| {rm_name} | {rm_status} | {reg_status} | {gap} |\n"

for reg_name, reg_status in registry_names.items():
    if reg_name not in capabilities_in_roadmap:
        gap_md += f"| {reg_name} | Missing from Roadmap | {reg_status} | YES |\n"

with open(os.path.join(audit_dir, "Gap_Report.md"), "w", encoding="utf-8") as f:
    f.write(gap_md)

# 6. Answer the 10 Questions
q_md = "# Master Audit Answers\n\n"

planned_not_started = [name for name, status in capabilities_in_roadmap.items() if status == "planned"]
q_md += "## 1. What was planned but never started?\n" + "\n".join([f"- {x}" for x in planned_not_started]) + "\n\n"

started_not_finished = [name for name, status in registry_names.items() if status == "in_progress"]
q_md += "## 2. What was started but never finished?\n" + "\n".join([f"- {x}" for x in started_not_finished]) + "\n\n"

implemented_not_doc = [v.get("name", k) for k, v in inventory["Capabilities"].items() if v.get("implementation_status") == "implemented" and not v.get("documentation_profile")]
q_md += "## 3. What was implemented but never documented?\n" + "\n".join([f"- {x}" for x in implemented_not_doc]) + "\n\n"

# 7. Generate Master Inventory MD
master_md = "# Master Inventory\n\n"
for phase, waves in inventory["Phases"].items():
    master_md += f"## {phase}\n"
    for wave, caps in waves.items():
        master_md += f"### {wave}\n"
        for cap in caps:
            master_md += f"- [{cap['Status']}] {cap['Name']} (Source: {cap['Source']})\n"
            
with open(os.path.join(audit_dir, "Master_Inventory.md"), "w", encoding="utf-8") as f:
    f.write(master_md)
    f.write("\n\n" + q_md)

print("Real structured audit complete.")
