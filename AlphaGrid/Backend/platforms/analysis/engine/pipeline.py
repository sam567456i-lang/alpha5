from Backend.platforms.analysis.core.dto import AnalysisContext, AnalysisResult
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
