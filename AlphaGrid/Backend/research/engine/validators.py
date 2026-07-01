"""Validators for Advanced Research Engines."""

from typing import Any, Dict
from Backend.research.engine.strategy_interface import STRATEGY_REGISTRY


class ValidationError(ValueError):
    """Raised when validation fails."""
    pass


class StrategyValidator:
    """Validates strategy parameters against their schema."""

    @staticmethod
    def validate_parameters(strategy_id: str, parameters: Dict[str, Any]) -> None:
        """Validates concrete parameters against the strategy's schema."""
        strategy_cls = STRATEGY_REGISTRY.get_strategy(strategy_id)
        schema = strategy_cls.get_parameter_schema()

        # Check for missing required parameters
        for param_name, constraints in schema.items():
            if constraints.get("required", False) and param_name not in parameters:
                raise ValidationError(f"Missing required parameter '{param_name}' for strategy '{strategy_id}'.")

        # Check for unsupported parameters, type correctness, and bounds
        for param_name, value in parameters.items():
            if param_name not in schema:
                raise ValidationError(f"Unsupported parameter '{param_name}' provided for strategy '{strategy_id}'.")

            constraints = schema[param_name]
            expected_type = constraints.get("type")
            if expected_type and not isinstance(value, expected_type):
                # Allow int where float is expected
                if expected_type is float and isinstance(value, int):
                    pass
                else:
                    raise ValidationError(f"Invalid type for parameter '{param_name}'. Expected {expected_type.__name__}, got {type(value).__name__}.")

            # Bounds checking
            min_val = constraints.get("min")
            if min_val is not None and value < min_val:
                raise ValidationError(f"Parameter '{param_name}' value {value} is below minimum {min_val}.")

            max_val = constraints.get("max")
            if max_val is not None and value > max_val:
                raise ValidationError(f"Parameter '{param_name}' value {value} is above maximum {max_val}.")


class WalkForwardValidator:
    """Validates walk-forward configuration."""

    @staticmethod
    def validate_config(config: Dict[str, Any]) -> None:
        required_keys = ["min_training_period", "min_testing_period", "step_size"]
        for key in required_keys:
            if key not in config:
                raise ValidationError(f"Missing required walk-forward config key: '{key}'")
            if not isinstance(config[key], int) or config[key] <= 0:
                raise ValidationError(f"Walk-forward config '{key}' must be a positive integer (representing days).")

        if config["step_size"] > config["min_training_period"]:
            raise ValidationError("Walk-forward step_size cannot be greater than min_training_period (leads to massive data gaps).")


class MonteCarloValidator:
    """Validates Monte Carlo configuration."""

    @staticmethod
    def validate_config(config: Dict[str, Any], strategy_id: str) -> None:
        required_keys = ["num_iterations", "perturbations"]
        for key in required_keys:
            if key not in config:
                raise ValidationError(f"Missing required Monte Carlo config key: '{key}'")

        if not isinstance(config["num_iterations"], int) or config["num_iterations"] <= 0:
            raise ValidationError("Monte Carlo 'num_iterations' must be a positive integer.")

        perturbations = config["perturbations"]
        if not isinstance(perturbations, dict):
            raise ValidationError("Monte Carlo 'perturbations' must be a dictionary.")

        # Ensure perturbed parameters exist in strategy schema
        strategy_cls = STRATEGY_REGISTRY.get_strategy(strategy_id)
        schema = strategy_cls.get_parameter_schema()

        seen_params = set()
        for param_name, perturb_config in perturbations.items():
            if param_name not in schema:
                raise ValidationError(f"Cannot perturb unsupported parameter '{param_name}' in strategy '{strategy_id}'.")
            if param_name in seen_params:
                raise ValidationError(f"Duplicate optimization parameter in Monte Carlo config: '{param_name}'.")
            seen_params.add(param_name)

            if "type" not in perturb_config or perturb_config["type"] not in ("gaussian", "uniform", "discrete"):
                raise ValidationError(f"Invalid perturbation type for '{param_name}'. Must be 'gaussian', 'uniform', or 'discrete'.")
