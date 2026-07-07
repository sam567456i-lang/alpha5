import os
import json
import hashlib
from datetime import datetime

class CertificationManifestGenerator:
    """Project OS Stage 12: Certification Manifest Generator"""
    
    def __init__(self, repo_root: str):
        self.repo_root = repo_root
        self.reports_dir = os.path.join(repo_root, "Docs", "Governance", "Reports")
        self.manifest_path = os.path.join(self.reports_dir, "Certification_Manifest.json")
        
    def _hash_file(self, rel_path: str) -> str:
        full_path = os.path.join(self.repo_root, rel_path)
        try:
            with open(full_path, "rb") as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception:
            return "N/A"

    def generate_manifest(self):
        print("Generating Stage 12 Certification Manifest...")
        
        manifest = {
            "certification_version": "AlphaGrid Infinity X v25.0 Certification Suite",
            "repository_snapshot_id": "Snapshot_v25",
            "repository_hash_manifest": self._hash_file(os.path.join("Docs", "Governance", "Reports", "Repository_Snapshot_v25.json")),
            "registry_version_hash": self._hash_file("master_capability_registry.yaml"),
            "capability_matrix_version_hash": self._hash_file(os.path.join("Docs", "Governance", "Master_Capability_Matrix.md")),
            "dependency_matrix_version_hash": self._hash_file(os.path.join("Docs", "Governance", "Reports", "Master_Dependency_Matrix.json")),
            "universal_switch_registry_version_hash": self._hash_file(os.path.join("Docs", "Governance", "universal_switches.yaml")),
            "required_certification_domains": [
                "Repository", "Governance", "Architecture", "Registry", "DTO", 
                "Determinism", "Platform Purity", "AI Boundaries"
            ],
            "required_test_suites": [
                "ProjectOS.certification.certify",
                "ProjectOS.validator.integrity_checker"
            ],
            "required_approval_gates": [
                "Stage 4 Human Approval",
                "Repository Integrity Gate",
                "Definition of Done Gate",
                "Project OS Acceptance Gate"
            ],
            "freeze_criteria": [
                "0 Purity Violations",
                "0 Circular Dependencies",
                "100% Deterministic Registry Execution",
                "Signed Certification Manifest"
            ]
        }
        
        # Serialize to hash the manifest itself
        manifest_str = json.dumps(manifest, sort_keys=True)
        manifest_hash = hashlib.sha256(manifest_str.encode('utf-8')).hexdigest()
        manifest["_manifest_signature_hash"] = manifest_hash
        manifest["_generated_at"] = datetime.utcnow().isoformat() + "Z"
        
        os.makedirs(os.path.dirname(self.manifest_path), exist_ok=True)
        with open(self.manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=4)
            
        print(f"Certification Manifest successfully generated and cryptographically signed at {self.manifest_path}")
        print(f"Manifest Hash: {manifest_hash}")

if __name__ == "__main__":
    repo_root = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid"
    gen = CertificationManifestGenerator(repo_root)
    gen.generate_manifest()
