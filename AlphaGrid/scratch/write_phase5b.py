import os
import yaml

BASE_DIR = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid"
P5_DIR = os.path.join(BASE_DIR, "Backend", "platforms", "analysis")

# 1. Update contracts.yaml to have a real schema for Analysis
contracts_path = os.path.join(BASE_DIR, "Governance", "contracts.yaml")
with open(contracts_path, "r") as f:
    contracts = yaml.safe_load(f)

contracts["analysis_contract"]["inputs"] = [
    {"name": "market_data", "type": "DataFrame", "required": True},
    {"name": "timeframe", "type": "str", "required": True},
    {"name": "parameters", "type": "Dict[str, Any]", "required": False}
]
contracts["analysis_contract"]["outputs"] = [
    {"name": "score", "type": "float", "description": "-1.0 to 1.0"},
    {"name": "signals", "type": "List[Signal]", "required": False},
    {"name": "raw_data", "type": "DataFrame", "required": True}
]
contracts["analysis_contract"]["invariants"] = [
    "score_between_minus_one_and_one",
    "raw_data_matches_input_index"
]

with open(contracts_path, "w") as f:
    yaml.dump(contracts, f, sort_keys=False)

# 2. Write DTOs
os.makedirs(os.path.join(P5_DIR, "core"), exist_ok=True)
dto_code = """from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import pandas as pd

@dataclass
class AnalysisContext:
    \"\"\"Universal context injected into every analysis.\"\"\"
    market_data: pd.DataFrame
    timeframe: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    dependencies: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AnalysisResult:
    \"\"\"Universal output from every analysis.\"\"\"
    score: float
    raw_data: pd.DataFrame
    signals: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AnalysisMetadata:
    \"\"\"Representation of the Governance capability registry entry.\"\"\"
    capability_id: str
    platform: str
    family: str
    subfamily: str
    dependencies: List[str]
"""
with open(os.path.join(P5_DIR, "core", "dto.py"), "w") as f:
    f.write(dto_code)
with open(os.path.join(P5_DIR, "core", "__init__.py"), "w") as f:
    f.write("from .dto import AnalysisContext, AnalysisResult, AnalysisMetadata\n")

# 3. Write Registry Loader
os.makedirs(os.path.join(P5_DIR, "registry"), exist_ok=True)
loader_code = """import yaml
import os
from Backend.platforms.analysis.core.dto import AnalysisMetadata

class RegistryLoader:
    def __init__(self, registry_path: str):
        self.registry_path = registry_path
        self._cache = {}
        self.load()
        
    def load(self):
        if not os.path.exists(self.registry_path):
            raise FileNotFoundError(f"Registry not found: {self.registry_path}")
        with open(self.registry_path, "r") as f:
            data = yaml.safe_load(f)
            
        for cap in data.get("capabilities", []):
            cid = cap.get("capability_id")
            if cid:
                self._cache[cid] = AnalysisMetadata(
                    capability_id=cid,
                    platform=cap.get("platform", "P05"),
                    family=cap.get("family", "Unknown"),
                    subfamily=cap.get("subfamily", "Unknown"),
                    dependencies=cap.get("dependencies", [])
                )
                
    def get_metadata(self, capability_id: str) -> AnalysisMetadata:
        if capability_id not in self._cache:
            raise ValueError(f"Capability {capability_id} not found in registry.")
        return self._cache[capability_id]
"""
with open(os.path.join(P5_DIR, "registry", "loader.py"), "w") as f:
    f.write(loader_code)
with open(os.path.join(P5_DIR, "registry", "__init__.py"), "w") as f:
    f.write("from .loader import RegistryLoader\n")

# 4. Write Factory
os.makedirs(os.path.join(P5_DIR, "factory"), exist_ok=True)
factory_code = """from typing import Type, Dict
from Backend.platforms.analysis.core.dto import AnalysisContext, AnalysisResult
from Backend.platforms.analysis.registry.loader import RegistryLoader

class BaseAnalysis:
    def execute(self, context: AnalysisContext) -> AnalysisResult:
        raise NotImplementedError()

class AnalysisFactory:
    def __init__(self, loader: RegistryLoader):
        self.loader = loader
        self._implementations: Dict[str, Type[BaseAnalysis]] = {}
        
    def register(self, capability_id: str, impl: Type[BaseAnalysis]):
        # Ensure it exists in registry first
        self.loader.get_metadata(capability_id) 
        self._implementations[capability_id] = impl
        
    def create(self, capability_id: str) -> BaseAnalysis:
        impl = self._implementations.get(capability_id)
        if not impl:
            raise ValueError(f"No implementation registered for {capability_id}")
        return impl()
"""
with open(os.path.join(P5_DIR, "factory", "factory.py"), "w") as f:
    f.write(factory_code)
with open(os.path.join(P5_DIR, "factory", "__init__.py"), "w") as f:
    f.write("from .factory import AnalysisFactory, BaseAnalysis\n")

# 5. Write Contract Validator
os.makedirs(os.path.join(P5_DIR, "validators"), exist_ok=True)
validator_code = """import yaml
import os
from Backend.platforms.analysis.core.dto import AnalysisContext, AnalysisResult

class ContractValidator:
    def __init__(self, contracts_path: str):
        with open(contracts_path, "r") as f:
            data = yaml.safe_load(f)
        self.analysis_contract = data.get("analysis_contract", {})
        
    def validate_input(self, context: AnalysisContext):
        # Extremely strict: check that pandas dataframe is not empty
        if context.market_data is None or context.market_data.empty:
            raise ValueError("Contract Violation: market_data cannot be empty")
        if not context.timeframe:
            raise ValueError("Contract Violation: timeframe is required")
            
    def validate_output(self, result: AnalysisResult):
        if not -1.0 <= result.score <= 1.0:
            raise ValueError(f"Contract Violation: score {result.score} outside [-1.0, 1.0]")
        if result.raw_data is None:
            raise ValueError("Contract Violation: raw_data is required")
"""
with open(os.path.join(P5_DIR, "validators", "contract_validator.py"), "w") as f:
    f.write(validator_code)
with open(os.path.join(P5_DIR, "validators", "__init__.py"), "w") as f:
    f.write("from .contract_validator import ContractValidator\n")

# 6. Write Pipeline and Engine
os.makedirs(os.path.join(P5_DIR, "engine"), exist_ok=True)
pipeline_code = """from Backend.platforms.analysis.core.dto import AnalysisContext, AnalysisResult
from Backend.platforms.analysis.validators.contract_validator import ContractValidator
from Backend.platforms.analysis.factory.factory import BaseAnalysis

class AnalysisPipeline:
    def __init__(self, validator: ContractValidator):
        self.validator = validator
        
    def run(self, analysis: BaseAnalysis, context: AnalysisContext) -> AnalysisResult:
        # 1. Validate Input
        self.validator.validate_input(context)
        # 2. Execute
        result = analysis.execute(context)
        # 3. Validate Output
        self.validator.validate_output(result)
        
        return result
"""
with open(os.path.join(P5_DIR, "engine", "pipeline.py"), "w") as f:
    f.write(pipeline_code)

engine_code = """from typing import Dict, List
from Backend.platforms.analysis.core.dto import AnalysisContext, AnalysisResult
from Backend.platforms.analysis.factory.factory import AnalysisFactory
from Backend.platforms.analysis.engine.pipeline import AnalysisPipeline

class AnalysisEngine:
    def __init__(self, factory: AnalysisFactory, pipeline: AnalysisPipeline):
        self.factory = factory
        self.pipeline = pipeline
        
    def run_batch(self, capability_ids: List[str], context: AnalysisContext) -> Dict[str, AnalysisResult]:
        results = {}
        for cid in capability_ids:
            try:
                analysis = self.factory.create(cid)
                res = self.pipeline.run(analysis, context)
                results[cid] = res
            except Exception as e:
                # Engine handles error recovery/logging (simplified for now)
                raise RuntimeError(f"Engine failed on {cid}: {str(e)}")
        return results
"""
with open(os.path.join(P5_DIR, "engine", "engine.py"), "w") as f:
    f.write(engine_code)
with open(os.path.join(P5_DIR, "engine", "__init__.py"), "w") as f:
    f.write("from .pipeline import AnalysisPipeline\nfrom .engine import AnalysisEngine\n")

print("Created Phase 5B Core Infrastructure successfully.")
