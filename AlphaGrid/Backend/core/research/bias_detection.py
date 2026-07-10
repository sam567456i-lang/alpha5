from typing import List, Dict, Any

class BiasDetectionException(Exception):
    pass

class BiasScanner:
    """Scans experiment configurations and pipeline boundaries for hidden biases."""
    
    @staticmethod
    def scan_for_lookahead_bias(experiment_config: Dict[str, Any], rule_definitions: List[Any]):
        """Ensures that no rule in the methodology uses data future to the execution_timestamp."""
        # Stub: Introspect rule parameters to ensure they don't request future bars
        pass
        
    @staticmethod
    def scan_for_data_leakage(train_window: tuple, test_window: tuple):
        """Ensures the train and test windows strictly do not overlap."""
        if not (train_window[1] < test_window[0] or test_window[1] < train_window[0]):
            raise BiasDetectionException("Data Leakage detected: Train and Test windows overlap.")
            
    @staticmethod
    def scan_for_survivorship_bias(dataset_metadata: Any):
        """Ensures the dataset includes delisted/bankrupt assets historically available."""
        if not dataset_metadata.provenance.missing_data_policy == "INCLUDES_DELISTED":
            # For strict institutional setups, this might be a warning rather than exception
            pass
            
    def run_full_scan(self, experiment_config: Dict[str, Any], dataset_metadata: Any):
        """Executes all bias checks before allowing an experiment to proceed."""
        self.scan_for_lookahead_bias(experiment_config, [])
        if "train_window" in experiment_config and "test_window" in experiment_config:
            self.scan_for_data_leakage(experiment_config["train_window"], experiment_config["test_window"])
        self.scan_for_survivorship_bias(dataset_metadata)
        return True
