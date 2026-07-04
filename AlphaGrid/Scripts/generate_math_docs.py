import os
import importlib.util
import inspect
from pathlib import Path

def generate_docs():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    math_dir = os.path.join(base_dir, "Backend", "math")
    docs_dir = os.path.join(base_dir, "Docs", "Math")
    os.makedirs(docs_dir, exist_ok=True)
    
    doc_path = os.path.join(docs_dir, "Math_Primitives_Reference.md")
    
    with open(doc_path, "w") as f:
        f.write("# Mathematical Core Primitives\n\n")
        f.write("This document is auto-generated from the metadata exposed by pure mathematical primitives.\n\n")
        
        for root, _, files in os.walk(math_dir):
            for file in files:
                if file.endswith(".py") and file != "__init__.py" and file != "indicator_result.py":
                    module_name = file[:-3]
                    file_path = os.path.join(root, file)
                    
                    # Dynamically load the module
                    spec = importlib.util.spec_from_file_location(module_name, file_path)
                    module = importlib.util.module_from_spec(spec)
                    try:
                        spec.loader.exec_module(module)
                    except Exception as e:
                        continue
                        
                    for name, obj in inspect.getmembers(module):
                        if inspect.isfunction(obj) and name.startswith("calculate_"):
                            # To get metadata, we actually have to run it.
                            # But for this script, we can just parse the docstring or 
                            # we can run a dummy array if it doesn't crash on length 0.
                            try:
                                import numpy as np
                                res = obj(np.array([1.0, 2.0]), np.array([1, 2]), period=2)
                                meta = res.metadata
                                f.write(f"## {meta.get('name', name)}\n")
                                f.write(f"- **Version**: {res.version}\n")
                                f.write(f"- **Formula**: {meta.get('formula', 'N/A')}\n")
                                f.write(f"- **Complexity**: {res.complexity}\n")
                                f.write(f"- **Memory**: {res.memory_complexity}\n")
                                f.write(f"- **References**: {', '.join(meta.get('references', []))}\n")
                                f.write(f"- **Failure Modes**: {', '.join(meta.get('failure_modes', []))}\n\n")
                            except Exception:
                                pass

if __name__ == "__main__":
    generate_docs()
    print("Documentation generated.")
