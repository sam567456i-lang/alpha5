import os
import sys

# Add project root to PYTHONPATH
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from Backend.indicator_engine.registry import IndicatorRegistry
# Import all engines to trigger registration
from Backend.indicator_engine import *

def generate_catalog():
    docs_dir = os.path.join(project_root, "Docs", "Architecture")
    os.makedirs(docs_dir, exist_ok=True)
    out_path = os.path.join(docs_dir, "indicator_catalog.md")
    
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("# AlphaGrid Indicator Catalog\n\n")
        f.write("This catalog is auto-generated from the Indicator Engine's Python runtime metadata.\n\n")
        f.write("## Inventory\n\n")
        
        for name, registration in sorted(IndicatorRegistry.get_all().items()):
            engine = registration["engine"]
            meta = getattr(engine, "metadata", {})
            
            f.write(f"### {name.upper()}\n")
            f.write(f"- **ID**: `{meta.get('id', name)}`\n")
            f.write(f"- **Family**: `{meta.get('family', 'Unknown')}`\n")
            f.write(f"- **Type**: `{meta.get('indicator_type', 'Unknown')}`\n")
            f.write(f"- **Composable**: `{meta.get('composable', False)}`\n")
            f.write(f"- **Streaming**: `{meta.get('streaming_supported', False)}`\n")
            f.write(f"- **Formula**: `{meta.get('formula', 'Unknown')}`\n")
            f.write(f"- **Inputs**: {meta.get('inputs', [])}\n")
            f.write(f"- **Outputs**: {meta.get('outputs', [])}\n")
            f.write(f"- **Warmup**: `{meta.get('warmup', 'Unknown')}`\n")
            f.write(f"- **Complexity**: `{meta.get('complexity', 'Unknown')}`\n")
            f.write(f"- **Deterministic**: `{meta.get('deterministic', True)}`\n\n")
            
    print(f"Successfully generated Indicator Catalog at {out_path}")

if __name__ == "__main__":
    generate_catalog()
