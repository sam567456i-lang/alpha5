import os

features_dir = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Backend\features"

for root, dirs, files in os.walk(features_dir):
    if "legacy" in dirs:
        dirs.remove("legacy")
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                
            if "if TYPE_CHECKING:" in content and "TYPE_CHECKING" not in content.split("if TYPE_CHECKING:")[0]:
                content = content.replace("from __future__ import annotations", "from __future__ import annotations\nfrom typing import TYPE_CHECKING")
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                    print(f"Fixed {file}")
