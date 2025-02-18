"""
Unit tests for usage module
"""
import pytest
from src.usage import (
    categorize_pool,
    CRITICAL_CATEGORY,
    LOW_CATEGORY
)

@pytest.mark.parametrize("pool,expected", [
    (
        {"id": "pool_1", "count": 5, "pool_count": 100},  # 5% usage
        CRITICAL_CATEGORY
    ),
    (
        {"id": "pool_2", "count": 20, "pool_count": 100},  # 20% usage
        LOW_CATEGORY
    ),
    (
        {"id": "pool_3", "count": 60, "pool_count": 100},  # 60% usage
        None
    ),
    (
        {"id": "pool_4"},  # Missing fields
        None
    ),
    (
        {"id": "pool_5", "count": "invalid", "pool_count": 100},  # Invalid count
        None
    ),
    (
        {"id": "pool_6", "count": 50, "pool_count": "invalid"},  # Invalid pool_count
        None
    )
])
def test_categorize_pool(pool, expected):
    """Test pool categorization logic"""
    assert categorize_pool(pool) == expected 