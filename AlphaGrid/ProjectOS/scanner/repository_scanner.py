import os
import hashlib
import time
from typing import Dict, List, Any

class RepositoryScanner:
    """Project OS Repository Scanner Engine (Certified for Stage 6)"""
    
    def __init__(self, repo_root: str):
        self.repo_root = repo_root
        
    def _hash_file(self, path: str) -> str:
        try:
            with open(path, "rb") as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception:
            return ""

    def scan_directory(self, target_dir: str, extensions: List[str] = [".md", ".yaml", ".py"]) -> List[Dict[str, str]]:
        """Deterministically scans a directory, enforcing Stage 5B rules."""
        target_path = os.path.join(self.repo_root, target_dir)
        if not os.path.exists(target_path):
            return []
            
        found_files = []
        for root, _, files in os.walk(target_path, followlinks=False):  # Symlink handling
            if ".git" in root or "__pycache__" in root or "node_modules" in root:
                continue
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    full_path = os.path.join(root, file)
                    # Exclude symlinks explicitly to prevent loops
                    if os.path.islink(full_path):
                        continue
                    found_files.append({
                        "path": full_path,
                        "hash": self._hash_file(full_path)
                    })
                    
        # Stable Output Ordering
        return sorted(found_files, key=lambda x: x["path"])
        
    def benchmark_scan(self) -> Dict[str, Any]:
        """Performance benchmark for scanning."""
        start = time.time()
        files = self.scan_directory(".")
        end = time.time()
        return {
            "duration_seconds": end - start,
            "files_scanned": len(files)
        }
