import os
import re

base_dir = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Backend"

for root, _, files in os.walk(base_dir):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Replace tags like [import-untyped], [arg-type], [override] that appear before a newline or # type: ignore
            new_content = re.sub(r"\s*\[(import-untyped|arg-type|override)\]", "", content)
            
            if new_content != content:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Cleaned {path}")
