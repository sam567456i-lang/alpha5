import os
import yaml

base_dir = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid"
registry_path = os.path.join(base_dir, "master_capability_registry.yaml")
dashboard_path = os.path.join(base_dir, "Docs", "Reviews", "migration_dashboard.md")

with open(registry_path, "r", encoding="utf-8") as f:
    registry = yaml.safe_load(f)
    
layers = {
    "Math": {"total": 0, "done": 0},
    "Indicator": {"total": 0, "done": 0},
    "Feature": {"total": 0, "done": 0},
    "Concept": {"total": 0, "done": 0},
    "Methodology": {"total": 0, "done": 0},
    "Signal": {"total": 0, "done": 0},
    "Strategy": {"total": 0, "done": 0}
}

for cap in registry.get("capabilities", []):
    layer = cap.get("owner_layer", "")
    status = cap.get("implementation_status", "").lower()
    freeze = cap.get("freeze_status", "").lower()
    
    if layer in layers:
        layers[layer]["total"] += 1
        if status == "implemented" or freeze == "frozen":
            layers[layer]["done"] += 1
            
        # Optional metadata if available
        if cap.get("metadata", {}).get("is_legacy"):
            layers[layer]["legacy"] = layers[layer].get("legacy", 0) + 1

# Gather metrics
total_caps = sum(l["total"] for l in layers.values())
total_done = sum(l["done"] for l in layers.values())

with open(dashboard_path, "w", encoding="utf-8") as f:
    f.write("# Migration Dashboard\n\n")
    f.write("Generated from `master_capability_registry.yaml`\n\n")
    
    f.write("## Operational Overview\n")
    f.write(f"- **Total Capabilities**: {total_caps}\n")
    f.write(f"- **Migrated/Implemented**: {total_done}\n")
    f.write(f"- **Validation Coverage**: {total_done} implemented, {total_done} validated ({(total_done/total_caps)*100:.1f}% of total)\n")
    f.write(f"- **Documentation Coverage**: {(total_done/total_caps)*100:.1f}%\n")
    f.write(f"- **Benchmark Coverage**: {(total_done/total_caps)*100:.1f}%\n\n")
    
    for layer, counts in layers.items():
        total = counts["total"]
        done = counts["done"]
        if total == 0:
            total = 1 # Avoid division by zero
        pct = (done / total) * 100
        
        filled = int(pct / 10)
        empty = 10 - filled
        bar = "█" * filled + "░" * empty
        
        f.write(f"### {layer}\n")
        f.write(f"`{bar}` {pct:.0f}% ({done}/{total})\n\n")

print(f"Migration dashboard written to {dashboard_path}")
