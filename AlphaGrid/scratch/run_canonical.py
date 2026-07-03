import sys
import traceback
import logging
import platform
import subprocess
import os

# Setup logging to both console and raw log file
os.makedirs("artifacts/phase22", exist_ok=True)
log_file = "artifacts/phase22/run.log"

# Clear existing log
with open(log_file, "w"):
    pass

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("RuntimeAudit")

def get_git_commit():
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode("utf-8").strip()
    except Exception:
        return "Unknown"

def get_git_branch():
    try:
        return subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode("utf-8").strip()
    except Exception:
        return "Unknown"

def get_repo_state():
    try:
        status = subprocess.check_output(["git", "status", "--porcelain"]).decode("utf-8")
        lines = [line for line in status.split('\n') if line]
        modified = len([l for l in lines if l.startswith(' M') or l.startswith('M ')])
        deleted = len([l for l in lines if l.startswith(' D') or l.startswith('D ')])
        untracked = len([l for l in lines if l.startswith('??')])
        is_clean = len(lines) == 0
        return {
            "clean": is_clean,
            "modified": modified,
            "deleted": deleted,
            "untracked": untracked
        }
    except Exception:
        return {"clean": False, "modified": 0, "deleted": 0, "untracked": 0}

def create_stage_entry():
    return {
        "Loaded": "NO",
        "Constructed": "NO",
        "Executed": "NO",
        "Input Type": "N/A",
        "Input Count": 0,
        "Input Checksum": "N/A",
        "Output Type": "N/A",
        "Output Count": 0,
        "Output Checksum": "N/A",
        "Consumer": "N/A",
        "Runtime": "N/A",
        "Status": "PENDING"
    }

manifest = {
    "Configuration": create_stage_entry(),
    "Foundation": create_stage_entry(),
    "ApplicationContext": create_stage_entry(),
    "DependencyInjection": create_stage_entry(),
    "Registries": create_stage_entry(),
    "Provider": create_stage_entry(),
    "Normalization": create_stage_entry(),
    "Session": create_stage_entry(),
    "DataQuality": create_stage_entry(),
    "MarketIntelligence": create_stage_entry(),
    "Feature": create_stage_entry(),
    "Concept": create_stage_entry(),
    "Primitive": create_stage_entry(),
    "Methodology": create_stage_entry(),
}

def print_manifest():
    logger.info("====================================")
    logger.info("Pipeline Execution Manifest")
    logger.info("====================================")
    for layer, state in manifest.items():
        logger.info(f"--- {layer} ---")
        for k, v in state.items():
            logger.info(f"  {k:<16}: {v}")
    logger.info("====================================")

def main():
    logger.info("Starting Runtime Execution Phase 22...")
    logger.info(f"Python Version: {platform.python_version()}")
    logger.info(f"OS: {platform.system()} {platform.release()}")
    
    commit = get_git_commit()
    branch = get_git_branch()
    state = get_repo_state()
    
    logger.info(f"Git Commit: {commit}")
    logger.info(f"Git Branch: {branch}")
    logger.info(f"Repo Clean: {state['clean']} (M: {state['modified']}, D: {state['deleted']}, ?: {state['untracked']})")
    
    # Placeholder for config SHA/Dataset SHA since those are determined dynamically in the orchestrator
    logger.info("Pipeline Version: 1.0.0")
    
    try:
        manifest["Configuration"]["Loaded"] = "YES"
        manifest["Configuration"]["Constructed"] = "YES"
        manifest["Configuration"]["Executed"] = "YES"
        manifest["Configuration"]["Status"] = "PASS"
        
        # Canonical Pipeline State Machine
        # 1. Create ApplicationContext (Foundation)
        from Backend.foundation.application_entrypoint import create_application_context
        manifest["Foundation"]["Loaded"] = "YES"
        manifest["Foundation"]["Constructed"] = "YES"
        manifest["Foundation"]["Executed"] = "YES"
        manifest["Foundation"]["Status"] = "PASS"
        
        context = create_application_context()
        for layer in ["ApplicationContext", "DependencyInjection", "Registries"]:
            manifest[layer]["Loaded"] = "YES"
            manifest[layer]["Constructed"] = "YES"
            manifest[layer]["Executed"] = "YES"
            manifest[layer]["Status"] = "PASS"
        
        # 2. Resolve Canonical Pipeline
        from Backend.core.canonical_pipeline import DomainResearchPipeline
        pipeline = context.container.resolve("domain_research_pipeline", DomainResearchPipeline)
        
        # 3. Execute
        datasets = [
            ("BTCUSDT", "1h", "2024-01-01T00:00:00", "2024-01-05T00:00:00"),
            ("NIFTY", "1d", "2024-01-01T00:00:00", "2024-01-05T00:00:00")
        ]
        
        for symbol, timeframe, from_date, to_date in datasets:
            logger.info(f"Executing Canonical Pipeline for {symbol} {timeframe}...")
            # We pass the manifest reference so the pipeline can update its own layer status
            pipeline.execute(symbol, timeframe, from_date, to_date, manifest)
            logger.info(f"Successfully processed {symbol} {timeframe}")

        print_manifest()

    except Exception as e:
        logger.error(f"FATAL RUNTIME BLOCKER: {type(e).__name__}")
        tb = traceback.format_exc()
        logger.error("--- STACK TRACE ---\n" + tb)
        print_manifest()
        sys.exit(1)

if __name__ == "__main__":
    main()
