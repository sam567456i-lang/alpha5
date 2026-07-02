"""Promotion Engine."""

from typing import Optional
from Backend.research.evaluation.report import ScientificEvaluationReport
from Backend.research.evaluation.registry import EvaluationRegistry
from Backend.research.experiments.registry import ResearchRegistry
from Shared.enums.experiment_status import ExperimentStatus

class PromotionEngine:
    """
    Routes ScientificEvaluationReports to the appropriate registries.
    Decoupled from the PromotionPolicy (which lives in the Evaluator).
    """

    def __init__(self, research_registry: Optional[ResearchRegistry] = None):
        # Allow injecting the research registry for testing/DI
        self.research_registry = research_registry if research_registry is not None else ResearchRegistry()

    def process(self, report: ScientificEvaluationReport) -> None:
        """
        Process the final report.
        1. Always register in the EvaluationRegistry (Audit Trail)
        2. If promoted, update the ResearchRegistry / CandidateRegistry
        """
        
        # 1. Audit Trail
        EvaluationRegistry.register(report)
        
        # 2. Routing
        if report.is_promoted:
            self.research_registry.log_experiment(
                hypothesis_id=report.hypothesis_id,
                experiment_id=report.experiment_id,
                config={}, # Would be passed from the orchestrator in real life
                status=ExperimentStatus.COMPLETED,
                metrics={"sharpe": report.risk.sharpe_ratio if report.risk else 0.0}
            )
            # In a full implementation, we'd also push to a CandidateRegistry class.
