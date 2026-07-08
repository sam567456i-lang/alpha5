import os
import glob
import re

def rename_and_update():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Backend"))
    docs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Docs"))
    
    p9_old = os.path.join(base_dir, "platforms", "platform9_features")
    p9_new = os.path.join(base_dir, "platforms", "platform9_concepts")
    
    p10_old = os.path.join(base_dir, "platforms", "platform10_concepts")
    p10_new = os.path.join(base_dir, "platforms", "platform10_methodologies")
    
    if os.path.exists(p9_old):
        os.rename(p9_old, p9_new)
        print(f"Renamed {p9_old} to {p9_new}")
    if os.path.exists(p10_old):
        os.rename(p10_old, p10_new)
        print(f"Renamed {p10_old} to {p10_new}")

    # Update imports
    py_files = glob.glob(os.path.join(base_dir, "**", "*.py"), recursive=True)
    md_files = glob.glob(os.path.join(docs_dir, "**", "*.md"), recursive=True)
    tests_dir = os.path.abspath(os.path.join(base_dir, "tests"))
    test_files = glob.glob(os.path.join(tests_dir, "**", "*.py"), recursive=True)
    
    for fpath in set(py_files + md_files + test_files):
        if not os.path.isfile(fpath): continue
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = content.replace("platform9_features", "platform9_concepts")
        new_content = new_content.replace("platform10_concepts", "platform10_methodologies")
        
        if new_content != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated imports in {fpath}")

if __name__ == "__main__":
    rename_and_update()
