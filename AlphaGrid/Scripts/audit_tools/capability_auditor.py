import os
import yaml
import json

def audit_capabilities():
    registry_dir = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Governance\registry"
    inventory_file = "inventory_report.json"
    
    with open(inventory_file, "r", encoding="utf-8") as f:
        inventory = json.load(f)
        
    classes = [c["name"] for c in inventory["classes"]]
    
    report = ["# Final Capability Audit Report\n"]
    report.append("This report audits the existence of every capability registered in the governance YAML against actual Python class implementations in the repository.\n")
    
    missing_capabilities = 0
    total_capabilities = 0
    
    for filename in os.listdir(registry_dir):
        if not filename.endswith(".yaml"):
            continue
            
        with open(os.path.join(registry_dir, filename), "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            
        report.append(f"## Registry: {filename}\n")
        
        # Traverse YAML structure dynamically
        if "analyses" in data:
            items = data["analyses"]
            id_key = "analysis_id"
        elif "features" in data:
            items = data["features"]
            id_key = "feature_id"
        elif "concepts" in data:
            items = data["concepts"]
            id_key = "concept_id"
        elif "methodologies" in data:
            items = data["methodologies"]
            id_key = "methodology_id"
        elif "engines" in data:
            items = data["engines"]
            id_key = "id"
        else:
            continue
            
        for item in items:
            total_capabilities += 1
            cap_id = item.get(id_key, "UNKNOWN")
            expected_class = "".join([word.capitalize() for word in cap_id.replace("ANA_", "").replace("ENG_", "").replace("METH_", "").split("_")])
            
            # Fuzzy match class existence
            found = any(expected_class.lower() in c.lower() for c in classes) or cap_id in str(inventory)
            
            status = "[x] Implemented" if found else "[ ] Missing Implementation"
            if not found:
                missing_capabilities += 1
                
            report.append(f"- {status} `{cap_id}` (Expected Class: {expected_class})")
            
        report.append("\n")
        
    report.append(f"### Summary\nTotal Capabilities Registered: {total_capabilities}\nMissing Implementations: {missing_capabilities}\n")
    
    with open("Capability_Audit_Report.md", "w", encoding="utf-8") as f:
        f.write("\n".join(report))
        
    print("Capability Audit Complete. Report Generated.")

if __name__ == "__main__":
    audit_capabilities()
