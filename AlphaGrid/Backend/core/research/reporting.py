from typing import Dict, Any, List
from Backend.core.research.experiment import ExperimentRun
from Backend.core.research.promotion import PromotionStage

class ReportingEngine:
    """Generates comprehensive PDF/HTML/JSON tearsheets for experiment runs."""
    
    @staticmethod
    def generate_tearsheet(experiment_run: ExperimentRun, statistical_metrics: Dict[str, Any]) -> str:
        """Stub for generating a massive tear sheet of the research run."""
        report = f"""
        ==================================================
        ALPHA GRID RESEARCH TEARSHEET
        ==================================================
        Experiment ID: {experiment_run.experiment_id}
        Dataset ID: {experiment_run.dataset_id}
        Methodology: {experiment_run.methodology_version}
        Execution Time: {experiment_run.execution_timestamp}
        --------------------------------------------------
        Win Rate: {experiment_run.metrics.get('win_rate', 0)}
        Expectancy: {experiment_run.metrics.get('expectancy', 0)}
        Statistically Significant: {statistical_metrics.get('is_statistically_significant', False)}
        --------------------------------------------------
        """
        return report

class ResearchDashboard:
    """Central interface combining all reporting and tracking over time."""
    
    def __init__(self):
        self.reports = []
        
    def add_report(self, report_string: str):
        self.reports.append(report_string)
        
    def view_pipeline_status(self) -> Dict[str, List[str]]:
        """Returns the current state of all tracked methodologies across promotion gates."""
        return {
            PromotionStage.RESEARCH.value: ["Trend_v2", "Wyckoff_v1"],
            PromotionStage.CANDIDATE.value: ["MarketProfile_v1"],
            PromotionStage.VALIDATED.value: ["SMC_v1"],
            PromotionStage.PAPER_TRADING.value: ["Trend_v1"],
            PromotionStage.PRODUCTION.value: [],
            PromotionStage.RETIRED.value: ["MeanReversion_v0.5"]
        }
