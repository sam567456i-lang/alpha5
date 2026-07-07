import os
import glob

def patch_versions(repo_root: str):
    engine_dir = os.path.join(repo_root, "Backend", "Platform15", "engine")
    
    for py_file in glob.glob(os.path.join(engine_dir, "*.py")):
        if py_file.endswith("__init__.py"):
            continue
            
        with open(py_file, "r") as f:
            content = f.read()
            
        # Very simple patch: find the class definition and insert the __version__ immediately after
        lines = content.splitlines()
        new_lines = []
        for line in lines:
            new_lines.append(line)
            if line.startswith("class "):
                new_lines.append("    __version__ = 'v1.0'")
                new_lines.append("    __dto_version__ = 'v1.0'")
                new_lines.append("    __schema_version__ = 'v1.0'")
                
        with open(py_file, "w") as f:
            f.write("\n".join(new_lines))
            
    print("Engines patched with version attributes.")

if __name__ == "__main__":
    repo = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid"
    patch_versions(repo)
