import os
import re

base_dir = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Backend\research\strategies\definitions"

for root, _, files in os.walk(base_dir):
    for file in files:
        if file.endswith(".py") and file != "__init__.py":
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Find the ID e.g., id="STRAT-RSI-001",
            match = re.search(r'id=["\']([^"\']+)["\'],', content)
            if match and "research_hypothesis_id=" not in content:
                strat_id = match.group(1)
                hyp_id = strat_id.replace("STRAT", "HYP")
                
                # inject research_hypothesis_id right after id
                new_content = content.replace(
                    match.group(0),
                    f'{match.group(0)}\n    research_hypothesis_id="{hyp_id}",'
                )
                
                if new_content != content:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"Updated {file} with hypothesis {hyp_id}")
