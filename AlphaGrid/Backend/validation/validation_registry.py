import yaml
import importlib
from typing import Dict, Any, List

class ValidationRegistry:
    def __init__(self, registry_path: str):
        self.registry_path = registry_path
        with open(registry_path, 'r') as f:
            self.data = yaml.safe_load(f)
            
        self.profiles = self.data.get('profiles', {})
        self.validators_config = self.data.get('validators', [])
        self._validators = {}
        
    def resolve_profile(self, profile_name: str) -> List[str]:
        if profile_name not in self.profiles:
            raise ValueError(f"Profile {profile_name} not found in registry.")
            
        raw_list = self.profiles[profile_name]
        resolved = []
        for item in raw_list:
            if item in self.profiles:
                resolved.extend(self.resolve_profile(item))
            else:
                resolved.append(item)
                
        # deduplicate while preserving order
        seen = set()
        final_list = []
        for x in resolved:
            if x not in seen:
                seen.add(x)
                final_list.append(x)
        return final_list
        
    def get_validator_config(self, validator_id: str) -> dict:
        for v in self.validators_config:
            if v['id'] == validator_id:
                return v
        raise ValueError(f"Validator {validator_id} not found in registry config.")
        
    def instantiate_validator(self, validator_id: str):
        config = self.get_validator_config(validator_id)
        class_name = config['class']
        
        try:
            # We map validator_id to module name. E.g. repository_validator -> repository_validator.py
            # For pipeline validators like e2e_pipeline_validator, we map to pipeline_validator if they are grouped,
            # but we generated individual files for them now via the script, so they all have their own file!
            module_name = validator_id
            
            # exception for pipeline_validator.py which has multiple classes in it:
            if "pipeline" in validator_id and validator_id != "pipeline_validator":
                module_name = "pipeline_validator"
                
            module = importlib.import_module(f"Backend.validation.validators.{module_name}")
            validator_class = getattr(module, class_name)
            return validator_class(validator_id=validator_id, config=config)
        except Exception as e:
            raise ImportError(f"Failed to instantiate {class_name} for {validator_id} from {module_name}: {e}")
