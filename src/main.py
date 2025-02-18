"""
Usage monitoring main module.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Query
from typing import Optional, List
from src.usage import (
    get_pools_usage, 
    get_last_execution, 
    CRITICAL_CATEGORY, 
    LOW_CATEGORY
)
from src.scheduler import start_scheduler, stop_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    # Startup
    start_scheduler()
    yield
    # Shutdown
    stop_scheduler()

app = FastAPI(title="Usage Monitoring", lifespan=lifespan)

@app.get("/pools")
async def get_usage(categories: Optional[List[str]] = Query(
    None,
    description="Filter pools by categories",
    enum=[CRITICAL_CATEGORY, LOW_CATEGORY]
)):
    """
    Get current usage statistics.
    
    Args:
        categories: Optional list of categories to filter by
        
    Returns:
        dict: A dictionary containing filtered usage statistics
    """
    result = await get_pools_usage()
    
    # If no categories specified or there's an error, return full result
    if not categories or "error" in result:
        return result
        
    # Filter usage_sets to only include requested categories
    filtered_sets = {
        category: result["usage_sets"][category]
        for category in categories
        if category in result["usage_sets"]
    }
    
    return {
        "timestamp": result["timestamp"],
        "usage_sets": filtered_sets
    }

@app.get("/last_execution")
def get_last_usage():
    """
    Get last pools usage statistics.
    Returns:
        dict: A dictionary containing last calculated usage statistics
    """
    return get_last_execution()

def main():
    """Main entry point for the application."""
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()