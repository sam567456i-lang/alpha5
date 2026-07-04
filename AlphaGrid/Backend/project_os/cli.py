import os
import json
from engine.core import ProjectOSEngine
from reports.generator import ReportGenerator

def main():
    print("Booting Project OS...")
    engine = ProjectOSEngine()
    results = engine.run_stage1_pipeline()
    
    print("Generating Reports...")
    generator = ReportGenerator()
    generator.generate_all(results)
    
    print("Project OS Stage 1 Complete.")

if __name__ == "__main__":
    main()
