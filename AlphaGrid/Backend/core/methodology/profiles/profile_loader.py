import yaml
import json
import hashlib
import datetime
from typing import Dict, Any
from Backend.core.methodology.dto.methodology_identity import ProfileIdentity

class ProfileLoader:
    """
    Loads declarative YAML/JSON profiles and handles inheritance.
    """
    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        self.loaded_profiles: Dict[str, dict] = {}
        
    def _read_file(self, file_path: str) -> dict:
        with open(file_path, 'r', encoding='utf-8') as f:
            if file_path.endswith('.yaml') or file_path.endswith('.yml'):
                return yaml.safe_load(f)
            elif file_path.endswith('.json'):
                return json.load(f)
            else:
                raise ValueError("Unsupported profile format. Use .yaml or .json")
                
    def _resolve_inheritance(self, profile_data: dict) -> dict:
        parent_file = profile_data.get("parent")
        if not parent_file:
            return profile_data
            
        # Recursive resolution (simplified for now)
        parent_data = self._read_file(f"{self.base_dir}/{parent_file}")
        parent_resolved = self._resolve_inheritance(parent_data)
        
        # Merge dictionaries (child overrides parent)
        merged = parent_resolved.copy()
        merged.update(profile_data)
        return merged
        
    def load_profile(self, file_path: str) -> tuple[dict, ProfileIdentity]:
        raw_data = self._read_file(f"{self.base_dir}/{file_path}")
        resolved_data = self._resolve_inheritance(raw_data)
        
        # Generate Identity
        data_str = json.dumps(resolved_data, sort_keys=True)
        profile_hash = hashlib.sha256(data_str.encode('utf-8')).hexdigest()
        
        identity = ProfileIdentity(
            id=resolved_data.get("id", "unknown"),
            semantic_version=resolved_data.get("version", "1.0.0"),
            hash=profile_hash,
            parent=resolved_data.get("parent"),
            created=datetime.datetime.now(datetime.timezone.utc),
            author=resolved_data.get("author", "system"),
            compatibility=resolved_data.get("compatibility", ">=1.0.0"),
            signature="unsigned"
        )
        
        return resolved_data, identity
