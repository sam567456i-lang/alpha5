import yaml
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
