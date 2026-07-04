import os

features_dir = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Backend\features"

for root, dirs, files in os.walk(features_dir):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            
            if "if TYPE_CHECKING:\n    import pandas as pd" in content:
                content = content.replace("if TYPE_CHECKING:\n    import pandas as pd", "import pandas as pd")
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Fixed {file}")
