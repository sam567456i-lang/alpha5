import sys
import traceback

def execute_pipeline():
    print("Initializing AlphaGrid Repository Execution...")
    
    try:
        # Step 1: Initialize Database and Registries
        print("\n[1] Initializing Database & Registries...")
        from Backend.foundation.database_manager import DatabaseManager
        db = DatabaseManager()
        db.connect()
        print("Database connected.")
        
        # Step 2: Ingest Raw Dataset
        print("\n[2] Ingesting Raw Dataset...")
        from Backend.market_intelligence.providers.abstract_market_data_provider import HistoricalDataProvider
        # Attempt to find a concrete provider
        print("Searching for concrete Market Data Provider...")
        # (We deleted Backend.market which had the Yahoo provider. The Intelligence engine has no concrete providers yet.)
        
        # Step 3: Run the Canonical E2E pipeline
        print("\n[3] Executing Normalization Engine...")
        from Backend.market_intelligence.normalization_engine import NormalizationEngine
        norm = NormalizationEngine()
        norm.normalize(raw_data=None)  # Will fail if it actually tries to do pandas ops on None
        
        print("\n[4] Executing Concept Engine...")
        from Backend.concepts.order_blocks.detector import OrderBlockDetector
        detector = OrderBlockDetector()
        
    except Exception as e:
        print(f"\nFATAL EXECUTION FAILURE: {type(e).__name__}")
        print("Stack Trace:")
        traceback.print_exc(file=sys.stdout)
        sys.exit(1)

if __name__ == "__main__":
    execute_pipeline()
