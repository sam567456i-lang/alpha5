import yaml
import os

BASE_DIR = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid"
GOV_DIR = os.path.join(BASE_DIR, "Governance")
DOCS_DIR = os.path.join(BASE_DIR, "Docs")

def generate_roadmap():
    with open(os.path.join(GOV_DIR, "master_capability_registry.yaml"), "r") as f:
        registry = yaml.safe_load(f)
        
    roadmap_path = os.path.join(DOCS_DIR, "master_roadmap.md")
    
    with open(roadmap_path, "w") as f:
        f.write("# AlphaGrid Master Roadmap (Auto-Generated)\n\n")
        f.write("This document is generated from Governance/master_capability_registry.yaml. Do not edit manually.\n\n")
        
        f.write("## Registered Capabilities\n")
        for cap in registry.get("capabilities", []):
            f.write(f"- **{cap['id']}**: {cap['name']} ({cap['maturity']})\n")
            
def generate_bible():
    with open(os.path.join(GOV_DIR, "master_taxonomy.yaml"), "r") as f:
        taxonomy = yaml.safe_load(f)
        
    bible_path = os.path.join(BASE_DIR, "Project_Bible.md")
    
    with open(bible_path, "w") as f:
        f.write("# AlphaGrid Project Bible (Auto-Generated)\n\n")
        f.write("This document is generated from Governance/master_taxonomy.yaml. Do not edit manually.\n\n")
        
        for key, value in taxonomy.items():
            if isinstance(value, list) and len(value) > 0:
                f.write(f"## {key.replace('_', ' ').title()}\n")
                for item in value:
                    f.write(f"- {item}\n")
                f.write("\n")

if __name__ == "__main__":
    generate_roadmap()
    generate_bible()
    print("Successfully generated markdown documentation from YAML Governance sources.")
