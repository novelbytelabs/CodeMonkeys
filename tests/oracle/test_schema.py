"""Tests for work order schema validation."""
import json
from pathlib import Path

import pytest

try:
    from jsonschema import validate, ValidationError
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False


SCHEMA_PATH = Path("nexus/schemas/work_order.schema.json")
WORK_ORDERS_DIR = Path("nexus/work_orders")


@pytest.fixture
def work_order_schema():
    """Load the work order schema."""
    with open(SCHEMA_PATH) as f:
        return json.load(f)


@pytest.fixture
def valid_work_order():
    """A valid work order for testing."""
    return {
        "job_id": "wo_codemonkeys-cli_validate_001",
        "product_id": "codemonkeys-cli",
        "intent": "validate",
        "inputs": {},
        "budget": {"max_actions": 1, "max_seconds": 60},
        "stop_conditions": ["on_silverback_fail", "on_missing_evidence"],
        "priority": 10,
        "created_at": "2025-12-22T12:00:00Z",
        "constitution_refs": ["constitution.md"],
        "evidence_expectations": ["dash/runs/codemonkeys-cli/last_run.json"]
    }


class TestWorkOrderSchema:
    """Tests for work order JSON schema."""

    @pytest.mark.skipif(not HAS_JSONSCHEMA, reason="jsonschema not installed")
    def test_schema_file_exists(self):
        """Schema file must exist."""
        assert SCHEMA_PATH.exists(), f"Schema not found: {SCHEMA_PATH}"

    @pytest.mark.skipif(not HAS_JSONSCHEMA, reason="jsonschema not installed")
    def test_schema_is_valid_json(self, work_order_schema):
        """Schema must be valid JSON."""
        assert "$schema" in work_order_schema
        assert "properties" in work_order_schema

    @pytest.mark.skipif(not HAS_JSONSCHEMA, reason="jsonschema not installed")
    def test_valid_work_order_passes(self, work_order_schema, valid_work_order):
        """Valid work order should pass validation."""
        validate(instance=valid_work_order, schema=work_order_schema)

    @pytest.mark.skipif(not HAS_JSONSCHEMA, reason="jsonschema not installed")
    def test_missing_required_field_fails(self, work_order_schema, valid_work_order):
        """Work order missing required field should fail."""
        del valid_work_order["job_id"]
        with pytest.raises(ValidationError):
            validate(instance=valid_work_order, schema=work_order_schema)

    @pytest.mark.skipif(not HAS_JSONSCHEMA, reason="jsonschema not installed")
    def test_invalid_intent_fails(self, work_order_schema, valid_work_order):
        """Work order with invalid intent should fail."""
        valid_work_order["intent"] = "invalid_intent"
        with pytest.raises(ValidationError):
            validate(instance=valid_work_order, schema=work_order_schema)

    @pytest.mark.skipif(not HAS_JSONSCHEMA, reason="jsonschema not installed")
    def test_validate_intent(self, work_order_schema, valid_work_order):
        """Validate intent should be accepted."""
        valid_work_order["intent"] = "validate"
        validate(instance=valid_work_order, schema=work_order_schema)

    @pytest.mark.skipif(not HAS_JSONSCHEMA, reason="jsonschema not installed")
    def test_test_intent(self, work_order_schema, valid_work_order):
        """Test intent should be accepted."""
        valid_work_order["intent"] = "test"
        validate(instance=valid_work_order, schema=work_order_schema)

    @pytest.mark.skipif(not HAS_JSONSCHEMA, reason="jsonschema not installed")
    def test_regenerate_report_intent(self, work_order_schema, valid_work_order):
        """Regenerate report intent should be accepted."""
        valid_work_order["intent"] = "regenerate_report"
        validate(instance=valid_work_order, schema=work_order_schema)

    @pytest.mark.skipif(not HAS_JSONSCHEMA, reason="jsonschema not installed")
    def test_empty_constitution_refs_fails(self, work_order_schema, valid_work_order):
        """Work order must have at least one constitution ref."""
        valid_work_order["constitution_refs"] = []
        with pytest.raises(ValidationError):
            validate(instance=valid_work_order, schema=work_order_schema)

    @pytest.mark.skipif(not HAS_JSONSCHEMA, reason="jsonschema not installed")
    def test_existing_work_orders_valid(self, work_order_schema):
        """All existing work orders must be valid."""
        for wo_file in WORK_ORDERS_DIR.glob("*.json"):
            if wo_file.name.startswith("_"):  # Skip meta files
                continue
            with open(wo_file) as f:
                wo = json.load(f)
            validate(instance=wo, schema=work_order_schema)
