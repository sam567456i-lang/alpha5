import os
import yaml
import json
from typing import Dict, Any, Optional

class ConfigurationLoader:
    """
    Strictly responsible for reading, parsing, and validating YAML/JSON files,
    and applying environment overrides. It does NOT manage active state.
    """
    def __init__(self, base_path: str = "config"):
        self.base_path = base_path

    def load_yaml(self, filename: str) -> Dict[str, Any]:
        filepath = os.path.join(self.base_path, f"{filename}.yaml")
        if not os.path.exists(filepath):
            filepath = os.path.join(self.base_path, f"{filename}.yml")
            if not os.path.exists(filepath):
                raise FileNotFoundError(f"Configuration file {filename} not found.")
                
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
            
        return self._apply_env_overrides(data)

    def load_json(self, filename: str) -> Dict[str, Any]:
        filepath = os.path.join(self.base_path, f"{filename}.json")
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Configuration file {filename} not found.")
            
        with open(filepath, 'r') as f:
            data = json.load(f)
            
        return self._apply_env_overrides(data)
        
    def _apply_env_overrides(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Applies environment variable overrides if they exist."""
        # Extremely simplistic override logic for structural demonstration
        for key, val in os.environ.items():
            if key.startswith("ALPHAGRID_"):
                # Parse ALPHAGRID_DB_HOST to ['db', 'host']
                parts = key[10:].lower().split('_')
                self._set_nested(config, parts, val)
        return config

    def _set_nested(self, config: Dict[str, Any], keys: list, value: Any):
        for key in keys[:-1]:
            config = config.setdefault(key, {})
        config[keys[-1]] = value
