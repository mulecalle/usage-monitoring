"""
Module for handling scheduled tasks.
"""
from apscheduler.schedulers.background import BackgroundScheduler
from src.usage import sync_get_pools_usage

# Initialize the scheduler
scheduler = BackgroundScheduler()

def init_scheduler():
    """Initialize scheduler with all required jobs."""
    # Run pools usage update every hour
    scheduler.add_job(sync_get_pools_usage, 'cron', hour='*/6')

def start_scheduler():
    """Start the scheduler."""
    init_scheduler()
    scheduler.start()

def stop_scheduler():
    """Stop the scheduler."""
    scheduler.shutdown() 