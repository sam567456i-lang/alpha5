import os
import shutil
import yaml
import csv

BASE_DIR = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid"
GOV_DIR = os.path.join(BASE_DIR, "Governance")

# 1. Move and modify validation_registry.yaml
val_src = os.path.join(BASE_DIR, "Docs", "Governance", "Validation_Registry.yaml")
val_dest = os.path.join(GOV_DIR, "validation_registry.yaml")

with open(val_src, "r") as f:
    val_data = yaml.safe_load(f)

new_val_data = {
    "schema_version": "1.0",
    "format_version": "1.0",
    "generated_by": "System",
    "generated_at": "2026-07-04T15:00:00Z",
    "checksum": "placeholder",
    "profiles": val_data.get("profiles", {})
}

with open(val_dest, "w") as f:
    yaml.dump(new_val_data, f, sort_keys=False)

# 2. Move capability matrix
matrix_src = os.path.join(BASE_DIR, "Docs", "Roadmaps", "Master_Capability_Matrix.csv")
matrix_dest = os.path.join(GOV_DIR, "master_capability_matrix.csv")
shutil.copy2(matrix_src, matrix_dest)

# 3. Move ADR
adr_dir = os.path.join(GOV_DIR, "adr")
os.makedirs(adr_dir, exist_ok=True)
adr_src = os.path.join(BASE_DIR, "Docs", "ADRs", "007_Platform_5_Universal_Taxonomy.md")
if os.path.exists(adr_src):
    shutil.copy2(adr_src, os.path.join(adr_dir, "007_Platform_5_Universal_Taxonomy.md"))

# 4. Move and modify master_capability_registry.yaml
reg_src = os.path.join(BASE_DIR, "master_capability_registry.yaml")
reg_dest = os.path.join(GOV_DIR, "master_capability_registry.yaml")

with open(reg_src, "r") as f:
    reg_data = yaml.safe_load(f)

new_reg_data = {
    "schema_version": "1.0",
    "format_version": "1.0",
    "generated_by": "System",
    "generated_at": "2026-07-04T15:00:00Z",
    "checksum": "placeholder",
    "capabilities": []
}

for cap in reg_data.get("capabilities", []):
    new_cap = {
        "id": cap.get("id", "UNKNOWN-ID"),
        "name": cap.get("name", "Unknown"),
        "version": cap.get("version", "1.0.0"),
        "maturity": "Planned",
        "relationships": {
            "hard_dependencies": cap.get("consumes", []),
            "soft_dependencies": [],
            "optional_dependencies": [],
            "conflicting_capabilities": [],
            "replaces": "",
            "deprecated_by": ""
        },
        "market_support": {
            "supported": cap.get("supported_markets", []),
            "unsupported": [],
            "placeholder": [],
            "required_feeds": ["Market Data"]
        },
        "streaming_support": {
            "batch": True,
            "streaming": False,
            "incremental": False,
            "warmup_required": 100,
            "stateful": False
        },
        "dashboard_contracts": {
            "searchable": ["id", "name"],
            "filterable": ["status"],
            "sortable": ["confidence"],
            "grouping": True,
            "export": True,
            "comparison": True
        },
        "cross_platform_references": {
            "adr": "007",
            "bible_section": "17"
        }
    }
    new_reg_data["capabilities"].append(new_cap)

with open(reg_dest, "w") as f:
    yaml.dump(new_reg_data, f, sort_keys=False)

# Delete old files
os.remove(val_src)
os.remove(matrix_src)
os.remove(reg_src)
if os.path.exists(adr_src):
    os.remove(adr_src)

print("Migration of Governance files complete.")
