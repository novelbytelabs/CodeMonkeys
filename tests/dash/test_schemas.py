import json
import pytest
import os

SCHEMA_VERSION = "0.1"

def load_json(path):
    assert os.path.exists(path), f"File not found: {path}"
    with open(path) as f:
        return json.load(f)

def test_products_json_validity():
    """AC-004: Validate products.json structure"""
    data = load_json("dash/products.json")
    
    # Schema checks
    assert data.get("schema_version") == SCHEMA_VERSION
    assert "generated_at" in data
    assert isinstance(data.get("products"), list)
    
    # Product entry checks
    for p in data["products"]:
        assert "product_id" in p
        assert "display_name" in p
        assert "repo" in p
        assert "path" in p
        assert "owner" in p
        assert "status" in p

def test_last_run_json_validity():
    """AC-004: Validate last_run.json structure"""
    product_id = "codemonkeys-dash"
    path = f"dash/runs/{product_id}/last_run.json"
    data = load_json(path)
    
    # Schema checks
    assert data.get("schema_version") == SCHEMA_VERSION
    assert data.get("product_id") == product_id
    assert "run_id" in data
    assert "started_at" in data
    assert "status" in data
    assert "summary" in data
    
    # Evidence checks
    assert "evidence" in data
    assert isinstance(data["evidence"].get("paths"), list)
    
    # Economy checks
    econ = data.get("banana_economy")
    assert econ is not None
    assert "budget_tokens" in econ
    assert "spent_tokens" in econ
    
    # Kill switch checks
    ks = data.get("kill_switch")
    assert ks is not None
    assert "enabled" in ks
