import os
import yaml

GOV_DIR = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Governance"

files_to_create = {
    "contracts": [
        "analysis_contract.yaml", "indicator_contract.yaml", "feature_contract.yaml",
        "concept_contract.yaml", "methodology_contract.yaml", "signal_contract.yaml",
        "opportunity_contract.yaml", "recommendation_contract.yaml", "dashboard_contract.yaml",
        "ai_contract.yaml"
    ],
    "rules": [
        "dependency_rules.yaml", "naming_rules.yaml", "versioning_rules.yaml",
        "freeze_rules.yaml", "documentation_rules.yaml", "validation_rules.yaml",
        "dashboard_rules.yaml", "ai_rules.yaml"
    ],
    "policies": [
        "security_policy.yaml", "licensing_policy.yaml", "external_repository_policy.yaml",
        "ai_policy.yaml", "release_policy.yaml", "deprecation_policy.yaml"
    ],
    "lifecycles": [
        "capability_lifecycle.yaml", "platform_lifecycle.yaml", "wave_lifecycle.yaml",
        "freeze_lifecycle.yaml", "external_repo_lifecycle.yaml", "dashboard_lifecycle.yaml"
    ]
}

def create_yaml(subfolder, filename):
    path = os.path.join(GOV_DIR, subfolder, filename)
    name = filename.replace("_", " ").replace(".yaml", "").title()
    content = {
        "name": name,
        "description": f"Standard {name.lower()} definition.",
        "version": "1.0.0"
    }
    
    if subfolder == "contracts":
        content["inputs"] = []
        content["outputs"] = []
        content["invariants"] = []
        
    with open(path, "w") as f:
        yaml.dump(content, f, sort_keys=False)

for subfolder, files in files_to_create.items():
    for f in files:
        create_yaml(subfolder, f)

# Update master taxonomy to add missing types
tax_path = os.path.join(GOV_DIR, "taxonomy", "master_taxonomy.yaml")
with open(tax_path, "r") as f:
    taxonomy = yaml.safe_load(f)

taxonomy.update({
    "indicator_families": ["Trend", "Momentum", "Volatility", "Volume"],
    "concept_families": ["Market Structure", "Price Action", "Smart Money"],
    "methodology_families": ["Wyckoff", "Elliott Wave", "VSA"],
    "signal_families": ["Reversal", "Continuation", "Breakout"],
    "strategy_families": ["Trend Following", "Mean Reversion", "Statistical Arbitrage"],
    "opportunity_types": ["Entry", "Exit", "Scale In", "Scale Out"],
    "risk_types": ["Stop Loss", "Trailing Stop", "Time Stop", "Volatility Stop"],
    "notification_types": ["Alert", "Warning", "Critical"],
    "dashboard_widget_types": ["Chart", "Table", "Heatmap", "Scanner", "AI Summary"],
    "validator_types": ["Unit", "Integration", "Property", "Dataset", "Regression"]
})

# Remove checksum from taxonomy
if "checksum" in taxonomy:
    del taxonomy["checksum"]
if "generated_at" in taxonomy:
    del taxonomy["generated_at"]

with open(tax_path, "w") as f:
    yaml.dump(taxonomy, f, sort_keys=False)

print("Created baseline YAMLs in contracts/, rules/, policies/, and lifecycles/.")
print("Expanded master_taxonomy.yaml.")
