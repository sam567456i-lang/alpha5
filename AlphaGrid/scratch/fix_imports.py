import os
import glob

def fix_imports():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Backend"))
    py_files = glob.glob(os.path.join(base_dir, "**", "*.py"), recursive=True)
    
    for fpath in py_files:
        if not os.path.isfile(fpath): continue
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            print(f"Skipping binary/non-utf8 file: {fpath}")
            continue
            
        new_content = content.replace("platform10_concepts", "platform10_methodologies")
        new_content = new_content.replace("platform10_methodologies.concept_", "platform9_concepts.concept_")
        
        if new_content != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated imports in {fpath}")

if __name__ == "__main__":
    fix_imports()
