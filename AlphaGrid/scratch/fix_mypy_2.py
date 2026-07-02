import os
import re

base_dir = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid"
mypy_ignores_to_remove = [
    (r"Backend\market\providers\yahoo.py", 40),
    (r"Backend\market\providers\angelone.py", 31),
    (r"Backend\api\middleware.py", 36),
    (r"Backend\ai\base_model.py", 37),
    (r"Backend\ai\trainer.py", 119),
    (r"Backend\cli\run_experiment.py", 13),
]

for rel_path, line_num in mypy_ignores_to_remove:
    path = os.path.join(base_dir, rel_path)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        idx = line_num - 1
        if 0 <= idx < len(lines):
            lines[idx] = re.sub(r"\s*# type: ignore.*", "\n", lines[idx])
            
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(lines)
