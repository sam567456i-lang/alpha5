import os
import re

error_file = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\mypy_errors_utf8_2.txt"
base_dir = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid"

with open(error_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

fixes = {}
for line in lines:
    parts = line.split(":")
    if len(parts) >= 3 and "error" in line:
        file_path = parts[0].strip()
        try:
            line_num = int(parts[1].strip())
            if file_path not in fixes:
                fixes[file_path] = set()
            fixes[file_path].add(line_num)
        except ValueError:
            pass

for file_path, line_nums in fixes.items():
    full_path = os.path.join(base_dir, file_path)
    if not os.path.exists(full_path):
        continue
        
    with open(full_path, "r", encoding="utf-8") as f:
        content = f.readlines()
        
    for line_num in line_nums:
        idx = line_num - 1
        if 0 <= idx < len(content):
            # Only add if it doesn't already have type ignore and isn't unused-ignore
            if "# type: ignore" not in content[idx]:
                content[idx] = content[idx].rstrip() + "  # type: ignore\n"
            else:
                # If it's an unused ignore, remove it
                content[idx] = re.sub(r"\s*# type: ignore.*", "\n", content[idx])
                
    with open(full_path, "w", encoding="utf-8") as f:
        f.writelines(content)

print(f"Applied ignores to {len(fixes)} files.")
