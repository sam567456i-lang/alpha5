from typing import Dict, List
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
