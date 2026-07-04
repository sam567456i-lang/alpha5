from typing import Dict, List
from Backend.platforms.analysis.core.dto import AnalysisContext, AnalysisResult
from Backend.platforms.analysis.factory.factory import AnalysisFactory
from Backend.platforms.analysis.engine.pipeline import AnalysisPipeline

class AnalysisEngine:
    def __init__(self, factory: AnalysisFactory, pipeline: AnalysisPipeline):
        self.factory = factory
        self.pipeline = pipeline
        
    def run_batch(self, capability_ids: List[str], context: AnalysisContext) -> Dict[str, AnalysisResult]:
        # Topological Sort (Simplified implementation for MVP)
        # We ensure capabilities that are dependencies of others run first.
        sorted_cids = []
        visited = set()
        
        def visit(cid):
            if cid in visited:
                return
            # Get metadata from registry
            meta = self.factory.registry.get_metadata(cid)
            if meta:
                for dep in meta.dependencies:
                    # Only sort if the dependency is also an Analysis module
                    if dep.startswith("ANALYSIS_") and dep in capability_ids:
                        visit(dep)
            visited.add(cid)
            sorted_cids.append(cid)
            
        for cid in capability_ids:
            visit(cid)
            
        results = {}
        for cid in sorted_cids:
            try:
                analysis = self.factory.create(cid)
                res = self.pipeline.run(analysis, context)
                results[cid] = res
                
                # ORCHESTRATOR INJECTION:
                # Inject the completed AnalysisResult into context.dependencies
                # so downstream Composite analyses can consume it.
                context.dependencies[cid] = res
                
            except Exception as e:
                raise RuntimeError(f"Engine failed on {cid}: {str(e)}")
        return results
