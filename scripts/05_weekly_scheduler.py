"""
Automated Weekly Update Scheduler
Runs data refresh and model retraining every week
Can be triggered by cron job, GitHub Actions, or cloud scheduler
"""

import subprocess
import json
from pathlib import Path
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/weekly_update.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def run_script(script_path, script_name):
    """Run a Python script and log results"""
    try:
        logger.info(f"Running {script_name}...")
        result = subprocess.run(
            ['python3', script_path],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            logger.info(f"✓ {script_name} completed successfully")
            return True
        else:
            logger.error(f"✗ {script_name} failed: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"✗ Error running {script_name}: {e}")
        return False

def automated_update():
    """Run complete update pipeline"""
    print("=" * 70)
    print("AUTOMATED WEEKLY UPDATE")
    print("=" * 70)
    
    logger.info("Starting weekly update cycle")
    
    Path('logs').mkdir(exist_ok=True)
    
    # Step 1: Fetch Vegas lines
    logger.info("\n[1/4] Fetching Vegas lines...")
    if not run_script('scripts/fetch_via_odds_api.py', 'Vegas Lines Fetcher'):
        logger.error("Failed to fetch Vegas lines, aborting")
        return False
    
    # Step 2: Enhanced analysis
    logger.info("\n[2/4] Running enhanced analysis...")
    if not run_script('scripts/02_enhanced_analysis.py', 'Enhanced Analysis'):
        logger.error("Failed to run enhanced analysis, aborting")
        return False
    
    # Step 3: Injury report
    logger.info("\n[3/4] Updating injury reports...")
    if not run_script('scripts/03_injury_report.py', 'Injury Report'):
        logger.error("Failed to update injury reports, continuing anyway")
    
    # Step 4: Retrain model
    logger.info("\n[4/4] Retraining model...")
    if not run_script('scripts/04_enhanced_model.py', 'Enhanced Model'):
        logger.error("Failed to retrain model, aborting")
        return False
    
    # Log completion
    update_log = {
        'timestamp': datetime.now().isoformat(),
        'status': 'success',
        'scripts_run': [
            'fetch_via_odds_api.py',
            '02_enhanced_analysis.py',
            '03_injury_report.py',
            '04_enhanced_model.py'
        ]
    }
    
    with open('logs/last_update.json', 'w') as f:
        json.dump(update_log, f, indent=2)
    
    logger.info("\n✓ Weekly update cycle complete!")
    logger.info("All data refreshed and model retrained")
    
    return True

if __name__ == '__main__':
    automated_update()

"""
DEPLOYMENT INSTRUCTIONS:

1. LOCAL TESTING:
   python3 scripts/05_weekly_scheduler.py

2. LINUX/MAC CRON JOB (Weekly, Monday 10 AM):
   0 10 * * 1 cd /path/to/model-game-totals && source venv/bin/activate && python3 scripts/05_weekly_scheduler.py

3. GITHUB ACTIONS (Automated workflow):
   Create .github/workflows/weekly-update.yml with:
   
   name: Weekly Model Update
   on:
     schedule:
       - cron: '0 10 * * 1'  # Monday 10 AM UTC
   
   jobs:
     update:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v2
         - uses: actions/setup-python@v2
           with:
             python-version: '3.11'
         - run: pip install -r scripts/requirements.txt
         - run: python3 scripts/05_weekly_scheduler.py
         - run: git add . && git commit -m "Weekly data update" && git push

4. VERCEL DEPLOYMENT:
   - Vercel will auto-rebuild when you push changes
   - Use GitHub Actions to automate pushes
   - Updated data will deploy within 2 minutes

5. MONITORING:
   - Check logs/weekly_update.log for details
   - Check logs/last_update.json for timestamp
   - Monitor dashboard for fresh predictions
"""
