import os, yaml
TAX = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Governance\taxonomy\master_taxonomy.yaml"
OUT = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Docs\Project_Bible.md"

with open(TAX, 'r') as f:
    tax = yaml.safe_load(f)

with open(OUT, 'w') as f:
    f.write("# AlphaGrid Project Bible\n\n")
    f.write("*(Auto-generated from Governance/taxonomy/master_taxonomy.yaml)*\n\n")
    for k, v in tax.items():
        if isinstance(v, list):
            f.write(f"## {k.replace('_', ' ').title()}\n")
            for item in v:
                f.write(f"- {item}\n")
            f.write("\n")
print("Generated Project_Bible.md")
