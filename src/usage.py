"""
Module for monitoring pools usage with scheduled checks.
"""
from datetime import datetime
import httpx
import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants for usage thresholds
CRITICAL_USAGE_THRESHOLD = 10
LOW_USAGE_THRESHOLD = 30

# Constants for categories
CRITICAL_CATEGORY = "critical"
LOW_CATEGORY = "low"

# Store timestamp for last execution
latest_execution = {
    "timestamp": None,
    "usage_sets": {
        CRITICAL_CATEGORY: [],
        LOW_CATEGORY: []
    }
}

def log_pools_summary(timestamp: str, pools_by_id: dict, usage_sets: dict):
    """
    Log a summary of pools usage.
    
    Args:
        timestamp: Current timestamp
        pools_by_id: Dictionary of pool data indexed by pool ID
        usage_sets: Dictionary of pool IDs categorized by usage level
    """
    logger.info("\n=== Pools Usage Summary ===")
    logger.info(f"Timestamp: {timestamp}\n")
    
    logger.info(f"Critical Pools ({len(usage_sets[CRITICAL_CATEGORY])}):")
    for pool_id in usage_sets[CRITICAL_CATEGORY]:
        pool = pools_by_id[pool_id]
        logger.info(f"  {pool_id}: {pool['count']}/{pool['pool_count']} ({(pool['count']/pool['pool_count'])*100:.1f}%)")
    
    logger.info(f"\nLow Usage Pools ({len(usage_sets[LOW_CATEGORY])}):")
    for pool_id in usage_sets[LOW_CATEGORY]:
        pool = pools_by_id[pool_id]
        logger.info(f"  {pool_id}: {pool['count']}/{pool['pool_count']} ({(pool['count']/pool['pool_count'])*100:.1f}%)")
    
    logger.info("\n========================")

def get_last_execution():
    """
    Get the last execution data.
    Returns:
        dict: Dictionary containing last execution data
    """
    return latest_execution

def categorize_pool(pool):
    """
    Categorize a pool based on its usage percentage.
    
    Args:
        pool: Dictionary containing pool data
        
    Returns:
        str or None: Category if pool data is valid, None if invalid
    """
    if 'count' not in pool or 'pool_count' not in pool:
        logger.warning(f"Pool {pool.get('id', 'UNKNOWN')} missing required fields (count/pool_count)")
        return None
    
    try:
        count = int(pool['count'])
        pool_count = int(pool['pool_count'])
        
        usage_percentage = (count / pool_count) * 100
        
        if usage_percentage <= CRITICAL_USAGE_THRESHOLD:
            return CRITICAL_CATEGORY
        elif usage_percentage <= LOW_USAGE_THRESHOLD:
            return LOW_CATEGORY
            
    except (ValueError, TypeError) as e:
        logger.warning(f"Pool {pool.get('id', 'UNKNOWN')} has invalid count/pool_count values: {str(e)}")
        return None

async def get_pools_usage():
    """
    Get the latest pools usage data from external service.
    Returns:
        dict: Dictionary containing pools usage data and timestamp
    """
    global latest_execution
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get('http://localhost:3000/pools')
            response.raise_for_status()
            pools_data = response.json()

            # Reset usage sets
            latest_execution["usage_sets"] = {
                CRITICAL_CATEGORY: [],
                LOW_CATEGORY: []
            }
            
            valid_pools = {}
            
            # Categorize each pool
            for pool in pools_data["pools"]:
                category = categorize_pool(pool)
                if category is not None:
                    latest_execution["usage_sets"][category].append(pool["id"])
                    valid_pools[pool["id"]] = pool
            
            latest_execution["timestamp"] = datetime.now().isoformat()
            
            # Log the summary using only valid pools
            log_pools_summary(
                latest_execution["timestamp"],
                valid_pools,
                latest_execution["usage_sets"]
            )
            
            return latest_execution
    except httpx.HTTPError as e:
        logger.error(f"HTTP error occurred: {str(e)}")
        return {"error": f"HTTP error occurred: {str(e)}", "status_code": e.response.status_code}
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return {"error": f"An error occurred: {str(e)}", "status_code": 503}

def sync_get_pools_usage():
    """Synchronous wrapper for get_pools_usage"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(get_pools_usage())
