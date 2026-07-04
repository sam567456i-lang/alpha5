import os
import re

features_dir = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Backend\features"

for root, dirs, files in os.walk(features_dir):
    if "legacy" in dirs:
        dirs.remove("legacy")
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                
            if "if TYPE_CHECKING:" in content and "TYPE_CHECKING" not in [x.strip() for x in re.findall(r'from typing import (.*)', content)[0].split(",")] if re.findall(r'from typing import (.*)', content) else False:
                # Need to add TYPE_CHECKING to typing import
                content = re.sub(r'from typing import (.*)', lambda m: f'from typing import {m.group(1)}, TYPE_CHECKING' if 'TYPE_CHECKING' not in m.group(1) else m.group(0), content)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                    print(f"Fixed TYPE_CHECKING import in {file}")
