"""
Unit tests for scheduler module
"""
import pytest
from src.scheduler import scheduler, init_scheduler, start_scheduler, stop_scheduler   

def test_scheduler_initialization():
    """Test scheduler initialization"""
    init_scheduler()
    jobs = scheduler.get_jobs()
    assert len(jobs) == 1
    job = jobs[0]
    assert job.trigger.fields[0].name == 'year'  # Check it's a cron trigger
    
def test_scheduler_lifecycle():
    """Test scheduler start and stop"""
    assert not scheduler.running
    start_scheduler()
    assert scheduler.running
    stop_scheduler()
    assert not scheduler.running 