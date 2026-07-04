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
                
            if "import pandas as pd" in content and "from typing import TYPE_CHECKING" not in content:
                content = "from __future__ import annotations\n" + content
                content = content.replace("from typing import Dict, Any, Optional", "from typing import Dict, Any, Optional, TYPE_CHECKING")
                content = content.replace("from typing import Dict, Any", "from typing import Dict, Any, TYPE_CHECKING")
                
                if "import pandas as pd\n" in content:
                    content = content.replace("import pandas as pd\n", "if TYPE_CHECKING:\n    import pandas as pd\n")
                
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                    print(f"Fixed imports in {file}")

