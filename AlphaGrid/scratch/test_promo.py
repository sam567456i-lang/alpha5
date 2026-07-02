import sys
from Backend.research.evaluation.report import ScientificEvaluationReport
from Backend.research.evaluation.metrics import MetricsCalculator, StatisticalMetrics
from Backend.research.evaluation.policy import PromotionPolicy
from Backend.research.evaluation.evaluator import ScientificEvaluator
from Backend.research.evaluation.promotion import PromotionEngine
from Backend.research.evaluation.registry import EvaluationRegistry
from Backend.research.experiments.registry import ResearchRegistry
from Shared.enums.experiment_status import ExperimentStatus

def run():
    EvaluationRegistry.clear()
    research_registry = ResearchRegistry()
    engine = PromotionEngine(research_registry=research_registry)
    
    evaluator = ScientificEvaluator(policy=PromotionPolicy(min_trades=5))
    
    pnls_pass = [10.0, 12.0, 8.0, 15.0, 5.0] * 2
    trades_pass = [{"pnl": p} for p in pnls_pass]
    
    # Promoted
    report_pass = evaluator.evaluate(
        experiment_id="EXP_PASS", hypothesis_id="RH_1",
        trades=trades_pass,
        equity_curve=[100.0 + i*10 for i in range(11)]
    )
    
    print(f"Report: {report_pass.is_promoted}")
    
    try:
        print(f"Before process. Engine registry ID: {id(engine.research_registry)}. Test registry ID: {id(research_registry)}")
        engine.process(report_pass)
        print(f"After process. Registry len(): {len(research_registry)}")
        print(f"After process. Registry get_all(): {research_registry.get_all()}")
        print(f"After process. Registry get_record(): {research_registry.get_record('EXP_PASS')}")
    except Exception as e:
        print(f"Exception! {e}")
        
    print(research_registry.get_record("EXP_PASS"))

if __name__ == "__main__":
    run()
