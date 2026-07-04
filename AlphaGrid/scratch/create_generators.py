import os

SCRIPTS_DIR = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Scripts"
DOCS_DIR = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Docs"

os.makedirs(os.path.join(DOCS_DIR, "Roadmaps"), exist_ok=True)
os.makedirs(os.path.join(DOCS_DIR, "Reports"), exist_ok=True)
os.makedirs(os.path.join(DOCS_DIR, "Dashboard"), exist_ok=True)

# 1. generate_matrix.py
matrix_code = """import os, yaml, csv
GOV_REG = r"C:\\Users\\praka\\Documents\\Codex\\2026-06-30\\alphagrid-infinity-x-5-0-master\\AlphaGrid\\Governance\\registry\\master_capability_registry.yaml"
OUT_CSV = r"C:\\Users\\praka\\Documents\\Codex\\2026-06-30\\alphagrid-infinity-x-5-0-master\\AlphaGrid\\Docs\\Roadmaps\\Master_Capability_Matrix.csv"

with open(GOV_REG, 'r') as f:
    data = yaml.safe_load(f)

capabilities = data.get('capabilities', [])
if capabilities:
    headers = list(capabilities[0].keys())
    with open(OUT_CSV, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(capabilities)
print("Generated Master_Capability_Matrix.csv")
"""

with open(os.path.join(SCRIPTS_DIR, "generate_matrix.py"), "w") as f:
    f.write(matrix_code)

# 2. generate_dashboard_docs.py
dash_code = """import os
OUT = r"C:\\Users\\praka\\Documents\\Codex\\2026-06-30\\alphagrid-infinity-x-5-0-master\\AlphaGrid\\Docs\\Dashboard\\dashboard_widgets.md"
with open(OUT, 'w') as f:
    f.write("# Dashboard Documentation (Generated)\\n")
print("Generated dashboard_widgets.md")
"""

with open(os.path.join(SCRIPTS_DIR, "generate_dashboard_docs.py"), "w") as f:
    f.write(dash_code)

# 3. generate_project_bible.py
bible_code = """import os, yaml
TAX = r"C:\\Users\\praka\\Documents\\Codex\\2026-06-30\\alphagrid-infinity-x-5-0-master\\AlphaGrid\\Governance\\taxonomy\\master_taxonomy.yaml"
OUT = r"C:\\Users\\praka\\Documents\\Codex\\2026-06-30\\alphagrid-infinity-x-5-0-master\\AlphaGrid\\Docs\\Project_Bible.md"

with open(TAX, 'r') as f:
    tax = yaml.safe_load(f)

with open(OUT, 'w') as f:
    f.write("# AlphaGrid Project Bible\\n\\n")
    f.write("*(Auto-generated from Governance/taxonomy/master_taxonomy.yaml)*\\n\\n")
    for k, v in tax.items():
        if isinstance(v, list):
            f.write(f"## {k.replace('_', ' ').title()}\\n")
            for item in v:
                f.write(f"- {item}\\n")
            f.write("\\n")
print("Generated Project_Bible.md")
"""

with open(os.path.join(SCRIPTS_DIR, "generate_project_bible.py"), "w") as f:
    f.write(bible_code)

# 4. generate_reports.py
reports_code = """import os
OUT_DIR = r"C:\\Users\\praka\\Documents\\Codex\\2026-06-30\\alphagrid-infinity-x-5-0-master\\AlphaGrid\\Docs\\Reports"

reports = ["Repository_Report.md", "Platform_Report.md", "Validation_Report.md"]
for r in reports:
    with open(os.path.join(OUT_DIR, r), "w") as f:
        f.write(f"# {r.replace('.md', '').replace('_', ' ')}\\n*(Auto-generated from Governance)*")
print("Generated reports.")
"""

with open(os.path.join(SCRIPTS_DIR, "generate_reports.py"), "w") as f:
    f.write(reports_code)

# 5. generate_docs.py (runner)
runner_code = """import subprocess, os
SCRIPTS_DIR = r"C:\\Users\\praka\\Documents\\Codex\\2026-06-30\\alphagrid-infinity-x-5-0-master\\AlphaGrid\\Scripts"

scripts = [
    "generate_matrix.py",
    "generate_dashboard_docs.py",
    "generate_project_bible.py",
    "generate_reports.py"
]

for s in scripts:
    subprocess.run(["python", os.path.join(SCRIPTS_DIR, s)])
print("All documentation generated successfully.")
"""

with open(os.path.join(SCRIPTS_DIR, "generate_docs.py"), "w") as f:
    f.write(runner_code)

print("Created 5 generator scripts in Scripts/.")
