"""
Schema validation tests for Dash MVP artifacts.
Validates JSON fixtures against formal JSON Schema files.
"""
import json
import os
import pytest

try:
    from jsonschema import validate, ValidationError
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False

SCHEMA_DIR = "dash/schemas"
FIXTURES = {
    "products": ("dash/products.json", "products.schema.json"),
    "last_run": ("dash/runs/codemonkeys-dash/last_run.json", "last_run.schema.json"),
}

def load_json(path):
    """Load JSON file and return parsed data."""
    assert os.path.exists(path), f"File not found: {path}"
    with open(path) as f:
        return json.load(f)

def load_schema(name):
    """Load JSON Schema file."""
    path = os.path.join(SCHEMA_DIR, name)
    return load_json(path)


@pytest.mark.skipif(not HAS_JSONSCHEMA, reason="jsonschema not installed")
def test_products_json_schema():
    """AC-004: Validate products.json against formal schema."""
    fixture_path, schema_name = FIXTURES["products"]
    data = load_json(fixture_path)
    schema = load_schema(schema_name)
    
    # This will raise ValidationError if invalid
    validate(instance=data, schema=schema)
    
    # Additional assertions
    assert data["schema_version"] == "0.1"
    assert len(data["products"]) >= 1


@pytest.mark.skipif(not HAS_JSONSCHEMA, reason="jsonschema not installed")
def test_last_run_json_schema():
    """AC-004: Validate last_run.json against formal schema."""
    fixture_path, schema_name = FIXTURES["last_run"]
    data = load_json(fixture_path)
    schema = load_schema(schema_name)
    
    # This will raise ValidationError if invalid
    validate(instance=data, schema=schema)
    
    # Additional assertions
    assert data["schema_version"] == "0.1"
    assert data["product_id"] == "codemonkeys-dash"


def test_products_json_structure():
    """Fallback test if jsonschema not available (inline checks)."""
    data = load_json("dash/products.json")
    
    assert data.get("schema_version") == "0.1"
    assert "generated_at" in data
    assert isinstance(data.get("products"), list)
    
    for p in data["products"]:
        assert "product_id" in p
        assert "display_name" in p
        assert "owner" in p
        assert "status" in p


def test_last_run_json_structure():
    """Fallback test if jsonschema not available (inline checks)."""
    data = load_json("dash/runs/codemonkeys-dash/last_run.json")
    
    assert data.get("schema_version") == "0.1"
    assert "run_id" in data
    assert "status" in data
    assert "evidence" in data
    assert isinstance(data["evidence"].get("paths"), list)
    assert "banana_economy" in data
    assert "kill_switch" in data
