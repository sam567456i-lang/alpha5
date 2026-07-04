import os
import re

files = [
    'Backend/math/public/sma.py',
    'Backend/math/public/wma.py',
    'Backend/math/public/rolling_sum.py',
    'Backend/math/public/variance.py',
    'Backend/math/public/stddev.py'
]

for f in files:
    with open(f, 'r') as file:
        content = file.read()
        
    func_name = f.split('/')[-1].split('.')[0]
    
    # 1. Bump version
    content = content.replace('version=\"1.0.0\"', 'version=\"1.1.0\"')
    
    # 2. Add update() stub
    stub = f"\n\ndef update_{func_name}(bar: Any, state: Dict[str, Any]) -> Any:\n    \"\"\"\n    Reserved streaming API for live execution.\n    \"\"\"\n    raise NotImplementedError(\"Streaming API reserved for future implementation.\")\n\ndef _build_empty_result"
    content = content.replace("\ndef _build_empty_result", stub)
    if "from typing import" not in content:
        content = content.replace("import numpy as np\n", "import numpy as np\nfrom typing import Any, Dict\n")
    else:
        if "Any" not in content:
            content = content.replace("from typing import ", "from typing import Any, ")
        if "Dict" not in content:
            content = content.replace("from typing import ", "from typing import Dict, ")
    
    # 3. Replace metadata
    # The metadata block usually ends before 'complexity="O(n)"'
    
    metadata_pattern = re.compile(r'metadata=\{(.*?)\},\s*complexity=', re.DOTALL)
    
    match = metadata_pattern.search(content)
    if match:
        old_metadata = match.group(1)
        
        # Extract name and short_name
        name_match = re.search(r'"name":\s*"(.*?)"', old_metadata)
        short_name_match = re.search(r'"short_name":\s*"(.*?)"', old_metadata)
        
        name = name_match.group(1) if name_match else func_name
        short_name = short_name_match.group(1) if short_name_match else func_name.upper()
        
        new_metadata = f'''metadata={{
            "name": "{name}",
            "short_name": "{short_name}",
            "inputs": ["close"],
            "output": ["values"],
            "warmup": period - 1,
            "deterministic": True,
            "precision": "1e-12",
            "complexity": "O(N)",
            "memory": "O(N)",
            "supports_nan": True,
            "supports_inf": True,
            "supports_streaming": False,
            "supports_incremental": False,
        }},
        complexity='''
        
        content = content[:match.start()] + new_metadata + content[match.end() - 11:]
        
    with open(f, 'w') as file:
        file.write(content)
    print(f"Updated metadata and streaming stub for {f}")

