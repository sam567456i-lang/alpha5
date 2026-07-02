"""Walk-Forward Optimization Engine."""

import logging
from typing import Any, Dict
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor

from Backend.research.engine.backtest import BacktestEngine
from Backend.research.engine.dataset_loader import DatasetLoader
from Backend.research.engine.strategy_interface import STRATEGY_REGISTRY
from Backend.research.models.experiment import Experiment


logger = logging.getLogger(__name__)


class WalkForwardEngine:
    """
    Executes walk-forward optimization over a dataset.
    Isolates Train (IS) and Test (OOS) windows to prevent lookahead bias.

    Architecture constraint: strictly 1 Experiment : 1 Strategy per run.
    The embargo_period config is validated against the strategy's declared
    max_label_horizon at startup to prevent silent label leakage.
    """

    def __init__(self, dataset_loader: DatasetLoader) -> None:
        self.dataset_loader = dataset_loader

    def _get_dataset_boundaries(self, snapshot_id: str, storage_path: str) -> tuple[datetime, datetime]:
        """Gets the absolute start and end times of the full dataset."""
        events = list(self.dataset_loader.load_and_verify(snapshot_id, storage_path))
        if not events:
            raise ValueError("Dataset is empty.")
        return events[0]["timestamp"], events[-1]["timestamp"]

    def execute(
        self, 
        base_experiment: Experiment, 
        storage_path: str, 
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Executes a walk-forward run.
        config requires: min_training_period, min_testing_period, step_size (in days),
                         embargo_period (timedelta, default timedelta(0))
        """
        min_train_days = config["min_training_period"]
        min_test_days = config["min_testing_period"]
        step_days = config["step_size"]
        mode = config.get("mode", "expanding") # "expanding" or "sliding"

        # Embargo period: timedelta typed. Defaults to 0 for reactive strategies.
        embargo = config.get("embargo_period", timedelta(0))
        if not isinstance(embargo, timedelta):
            raise TypeError(f"embargo_period must be a timedelta, got {type(embargo).__name__}")

        # Validate embargo against strategy's declared max_label_horizon.
        # Hard-fail if the configured embargo is insufficient for the strategy's
        # actual lookahead window — prevents silent label leakage.
        strategy_cls = STRATEGY_REGISTRY.get_strategy(base_experiment.strategy_id)
        required_horizon = strategy_cls.max_label_horizon()
        if embargo < required_horizon:
            raise ValueError(
                f"embargo_period ({embargo}) is less than strategy "
                f"{base_experiment.strategy_id}'s max_label_horizon ({required_horizon}). "
                f"This would cause label leakage across fold boundaries."
            )

        start_time, end_time = self._get_dataset_boundaries(base_experiment.dataset_snapshot_id, storage_path)

        folds = []
        current_train_end = start_time + timedelta(days=min_train_days)
        current_train_start = start_time
        fold_idx = 1

        while current_train_end + embargo + timedelta(days=min_test_days) <= end_time:
            # OOS starts AFTER the embargo gap following the IS window end.
            oos_start = current_train_end + embargo
            oos_end = oos_start + timedelta(days=min_test_days)
            
            folds.append({
                "fold_number": fold_idx,
                "is_start": current_train_start,
                "is_end": current_train_end,
                "oos_start": oos_start,
                "oos_end": oos_end
            })

            fold_idx += 1
            current_train_end += timedelta(days=step_days)
            
            if mode == "sliding":
                current_train_start += timedelta(days=step_days)

        if not folds:
            raise ValueError("Dataset not long enough to support even a single walk-forward fold.")

        results = []
        
        # We process folds concurrently. ThreadPoolExecutor isolates executions.
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = []
            for fold in folds:
                future = executor.submit(self._run_fold, base_experiment, storage_path, fold)
                futures.append((fold, future))
                
            for fold, future in futures:
                fold_res = future.result()
                results.append(fold_res)
                
        return {
            "experiment_id": str(base_experiment.id),
            "folds": results
        }
        
    def _run_fold(self, base_exp: Experiment, storage_path: str, fold: Dict[str, Any]) -> Dict[str, Any]:
        """Runs the IS and OOS isolated backtests for a given fold."""
        # IS Backtest
        is_engine = BacktestEngine()
        is_engine.execute(
            base_exp, 
            storage_path, 
            start_bound=fold["is_start"], 
            end_bound=fold["is_end"]
        )
        # OOS Backtest (Isolated instance, zero leakage)
        oos_engine = BacktestEngine()
        oos_engine.execute(
            base_exp, 
            storage_path, 
            start_bound=fold["oos_start"], 
            end_bound=fold["oos_end"]
        )
        
        # In a real system, metrics would be aggregated from the engine.
        return {
            "fold_number": fold["fold_number"],
            "is_start": fold["is_start"].isoformat(),
            "is_end": fold["is_end"].isoformat(),
            "oos_start": fold["oos_start"].isoformat(),
            "oos_end": fold["oos_end"].isoformat(),
            "is_metrics": {"mock": "metric"},
            "oos_metrics": {"mock": "metric"}
        }
