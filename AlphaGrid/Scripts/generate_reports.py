import os
OUT_DIR = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Docs\Reports"

reports = ["Repository_Report.md", "Platform_Report.md", "Validation_Report.md"]
for r in reports:
    with open(os.path.join(OUT_DIR, r), "w") as f:
        f.write(f"# {r.replace('.md', '').replace('_', ' ')}\n*(Auto-generated from Governance)*")
print("Generated reports.")
