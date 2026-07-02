"""Monte Carlo Simulation Engine."""

import logging
import copy
from typing import Any, Dict
from concurrent.futures import ThreadPoolExecutor

import numpy as np

from Backend.research.engine.backtest import BacktestEngine
from Backend.research.engine.dataset_loader import DatasetLoader
from Backend.research.models.experiment import Experiment


logger = logging.getLogger(__name__)


class MonteCarloEngine:
    """
    Executes Monte Carlo simulations via parameter perturbation and execution noise.
    Bootstrapping dataset is intentionally excluded per ADP to preserve temporal dependencies.
    """

    def __init__(self, dataset_loader: DatasetLoader) -> None:
        self.dataset_loader = dataset_loader

    def execute(
        self, 
        base_experiment: Experiment, 
        storage_path: str, 
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Executes Monte Carlo simulations.
        config requires: num_iterations, perturbations
        """
        num_iterations = config["num_iterations"]
        perturbations = config["perturbations"]
        
        # Derive strictly reproducible iteration seeds from the root seed
        root_seed = base_experiment.random_seed
        sq = np.random.SeedSequence(root_seed)
        iteration_seeds = sq.spawn(num_iterations)

        results = []
        
        # Run iterations concurrently
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = []
            for i in range(num_iterations):
                iteration_seed = int(iteration_seeds[i].generate_state(1)[0])
                
                # Clone base experiment and apply perturbations deterministically
                iter_exp = self._create_iteration_experiment(
                    base_experiment, 
                    iteration_seed, 
                    perturbations
                )
                
                future = executor.submit(self._run_iteration, iter_exp, storage_path, i)
                futures.append((i, future))
                
            for i, future in futures:
                iter_res = future.result()
                results.append(iter_res)
                
        return {
            "experiment_id": str(base_experiment.id),
            "iterations": results,
            "summary_metrics": {"mock": "distribution_stats"}
        }

    def _create_iteration_experiment(
        self, 
        base_exp: Experiment, 
        iteration_seed: int, 
        perturbations: Dict[str, Any]
    ) -> Experiment:
        """Clones experiment and mutates parameters deterministically via the iteration seed."""
        # Create a local RNG specifically for mutating parameters to guarantee reproducibility
        mutation_rng = np.random.default_rng(iteration_seed)
        
        new_params = copy.deepcopy(base_exp.parameters)
        
        for param_name, p_config in perturbations.items():
            p_type = p_config["type"]
            if p_type == "gaussian":
                mean = new_params.get(param_name, 0.0)
                std = p_config.get("std", 1.0)
                new_params[param_name] = mean + mutation_rng.normal(0, std)
            elif p_type == "uniform":
                low = p_config.get("low", 0.0)
                high = p_config.get("high", 1.0)
                new_params[param_name] = mutation_rng.uniform(low, high)
            elif p_type == "discrete":
                choices = p_config.get("choices", [])
                if choices:
                    new_params[param_name] = mutation_rng.choice(choices)
                    
        iter_exp = base_exp.model_copy(update={
            "random_seed": iteration_seed,
            "parameters": new_params
        })
        
        return iter_exp

    def _run_iteration(self, iter_exp: Experiment, storage_path: str, iteration_number: int) -> Dict[str, Any]:
        """Runs a single isolated Monte Carlo backtest iteration."""
        engine = BacktestEngine(dataset_loader=self.dataset_loader)
        engine.execute(iter_exp, storage_path)
        
        # In a real system, metrics would be fetched from the engine instance
        return {
            "iteration_number": iteration_number,
            "seed": iter_exp.random_seed,
            "parameters": iter_exp.parameters,
            "metrics": {"mock": "metric"}
        }
