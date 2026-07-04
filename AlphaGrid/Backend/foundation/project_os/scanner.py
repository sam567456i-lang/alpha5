import os
import csv
import yaml
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class RepositoryState:
    python_files: List[str]
    markdown_files: List[str]
    matrix_rows: List[Dict[str, str]]
    registry_data: Dict[str, Any]
    bible_content: str

class RepositoryScanner:
    """Scans the AlphaGrid repository to build the foundational state for the Project OS."""
    
    def __init__(self, base_dir: str):
        self.base_dir = base_dir

    def scan(self) -> RepositoryState:
        py_files = []
        md_files = []
        
        # Walk directories
        for root, _, files in os.walk(self.base_dir):
            if ".git" in root or "__pycache__" in root or "venv" in root:
                continue
            for f in files:
                full_path = os.path.join(root, f)
                if f.endswith(".py"):
                    py_files.append(full_path)
                elif f.endswith(".md"):
                    md_files.append(full_path)
                    
        # Load Matrix
        matrix_rows = []
        matrix_path = os.path.join(self.base_dir, "Docs", "Roadmaps", "Master_Capability_Matrix.csv")
        if os.path.exists(matrix_path):
            with open(matrix_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                matrix_rows = list(reader)
                
        # Load Registry
        registry_data = {}
        registry_path = os.path.join(self.base_dir, "master_capability_registry.yaml")
        if os.path.exists(registry_path):
            with open(registry_path, "r", encoding="utf-8") as f:
                registry_data = yaml.safe_load(f) or {}
                
        # Load Bible
        bible_content = ""
        bible_path = os.path.join(self.base_dir, "Project_Bible.md")
        if os.path.exists(bible_path):
            with open(bible_path, "r", encoding="utf-8") as f:
                bible_content = f.read()
                
        return RepositoryState(
            python_files=py_files,
            markdown_files=md_files,
            matrix_rows=matrix_rows,
            registry_data=registry_data,
            bible_content=bible_content
        )
