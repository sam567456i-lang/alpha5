class MethodologySDK:
    """
    Standard interface that every Platform 10 methodology plugin must implement.
    Ensures pure analytic evaluation with absolutely no trading/execution side-effects.
    """
    def __init__(self, methodology_id: str):
        self.methodology_id = methodology_id
        
    def validate_context(self, context) -> bool:
        """Determines if the methodology has enough data in the context to execute."""
        return True
        
    def get_capabilities(self) -> dict:
        """
        MUST be overridden by plugins to explicitly declare boundaries:
        - supported_concepts
        - unsupported_concepts
        - execution_modes
        - markets
        - asset_classes
        - deterministic
        - replay_supported
        - streaming_supported
        - minimum_registry_version
        - minimum_sdk_version
        """
        raise NotImplementedError("Plugins must declare capabilities")

    def evaluate(self, context):
        """
        Main execution block for a methodology plugin.
        Should return an assessment dict ready to be processed by the Builder and Quality engines.
        """
        raise NotImplementedError("Methodology plugins must implement evaluate()")
