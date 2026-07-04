import subprocess, os
SCRIPTS_DIR = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Scripts"

scripts = [
    "generate_matrix.py",
    "generate_dashboard_docs.py",
    "generate_project_bible.py",
    "generate_reports.py"
]

for s in scripts:
    subprocess.run(["python", os.path.join(SCRIPTS_DIR, s)])
print("All documentation generated successfully.")
