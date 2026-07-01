"""Backtest execution engine (ADP Sec 1, 9)."""

from typing import Any, Dict, Optional
from datetime import datetime
from uuid import UUID
import numpy as np

from Backend.research.models.experiment import Experiment
from Backend.research.models.result import BacktestResult
from Backend.research.engine.dataset_loader import DatasetLoader
from Backend.research.engine.strategy_interface import STRATEGY_REGISTRY


class BacktestEngine:
    """
    Executes an Experiment safely outside of any DB transaction.
    Guarantees chronological event ordering and lookahead bias prevention.
    """

    def __init__(self, dataset_loader: DatasetLoader = None) -> None:
        self.dataset_loader = dataset_loader or DatasetLoader()

    def execute(self, experiment: Experiment, snapshot_storage_path: str, start_bound: Optional[datetime] = None, end_bound: Optional[datetime] = None) -> BacktestResult:
        """
        Runs the backtest simulation in memory.
        
        Args:
            experiment: The deterministic experiment configuration.
            snapshot_storage_path: The disk path to the verified Parquet snapshot.
            start_bound: Optional start time for the backtest.
            end_bound: Optional end time for the backtest.
            
        Returns:
            BacktestResult produced fully in memory.
        """
        # 1. Instantiate Root RNG (ADP Section 9)
        # Exactly ONE root random seed persisted per experiment.
        root_rng = np.random.Generator(np.random.PCG64(experiment.random_seed))

        # 2. Resolve and Instantiate Strategy (ADP Section 10)
        strategy_cls = STRATEGY_REGISTRY.get_strategy(experiment.strategy_id)
        strategy = strategy_cls(parameters=experiment.parameters, random_generator=root_rng)

        # 3. Load and Verify Dataset (ADP Sections 3 & 4)
        # Returns an iterator that enforces chronological sequence.
        event_stream = self.dataset_loader.load_and_verify(
            snapshot_id=experiment.dataset_snapshot_id,
            storage_path=snapshot_storage_path,
            start_bound=start_bound,
            end_bound=end_bound
        )

        # 4. Event Loop (Event ordering & Lookahead bias prevention)
        # Lookahead bias is prevented structurally: the strategy only ever receives 
        # a single atomic event representing 'now', and cannot index into a global DataFrame.
        for event in event_stream:
            strategy.on_market_event(event)
            # Internal matching engine logic would go here.
            # Deferred to Slice 2B/C, currently focusing on engine foundation.

        # 5. Produce Final Result In-Memory (ADP Section 1)
        # Dummy metrics until the metrics engine (Slice 2B) is implemented.
        return BacktestResult(
            experiment_id=experiment.id,
            total_return=0.0,
            sharpe_ratio=0.0,
            max_drawdown=0.0,
            trades=[]
        )
