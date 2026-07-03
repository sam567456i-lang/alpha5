"""Dynamic Provider Factory for Historical Data Providers."""

import importlib
import pkgutil
from typing import Dict, Type
from Backend.market_intelligence.providers.abstract_market_data_provider import HistoricalDataProvider

class ProviderFactory:
    """Factory for instantiating market data providers based on configuration keys."""
    
    _providers: Dict[str, Type[HistoricalDataProvider]] = {}
    _discovered = False

    @classmethod
    def register(cls, key: str, provider_class: Type[HistoricalDataProvider]) -> None:
        """Register a provider class with a configuration key."""
        cls._providers[key] = provider_class

    @classmethod
    def create(cls, key: str) -> HistoricalDataProvider:
        """Create an instance of the requested provider."""
        if not cls._discovered:
            cls._discover_plugins()
            
        provider_class = cls._providers.get(key)
        if not provider_class:
            raise ValueError(
                f"Unknown historical provider configured: '{key}'. "
                f"Available providers: {list(cls._providers.keys())}"
            )
        return provider_class()

    @classmethod
    def _discover_plugins(cls) -> None:
        """Dynamically load all modules in the providers package to trigger their register() calls."""
        import Backend.market_intelligence.providers as providers_package
        package_name = providers_package.__name__
        package_path = providers_package.__path__
        
        for _, module_name, _ in pkgutil.iter_modules(package_path):
            if module_name not in ["abstract_market_data_provider", "provider_factory"]:
                try:
                    importlib.import_module(f"{package_name}.{module_name}")
                except Exception as e:
                    import logging
                    logging.warning(f"Failed to load provider plugin '{module_name}': {e}")
                    
        cls._discovered = True
