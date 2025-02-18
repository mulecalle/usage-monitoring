"""
Unit tests for main module
"""
import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_get_pools_no_filter():
    """Test /pools endpoint without category filter"""
    response = client.get("/pools")
    assert response.status_code == 200
    data = response.json()
    assert "timestamp" in data
    assert "usage_sets" in data
    assert "critical" in data["usage_sets"]
    assert "low" in data["usage_sets"]

@pytest.mark.parametrize("categories,expected_keys", [
    (["critical"], ["critical"]),
    (["low"], ["low"]),
    (["critical", "low"], ["critical", "low"])
])
def test_get_pools_with_filter(categories, expected_keys):
    """Test /pools endpoint with category filters"""
    params = [("categories", cat) for cat in categories]
    response = client.get("/pools", params=params)
    assert response.status_code == 200
    data = response.json()
    assert "timestamp" in data
    assert "usage_sets" in data
    assert set(data["usage_sets"].keys()) == set(expected_keys)

def test_get_last_execution():
    """Test /last_execution endpoint"""
    response = client.get("/last_execution")
    assert response.status_code == 200
    data = response.json()
    assert "timestamp" in data
    assert "usage_sets" in data 