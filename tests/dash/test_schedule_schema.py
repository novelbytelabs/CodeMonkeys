"""Tests for schedule schema validation."""
import json
from pathlib import Path

import pytest
from jsonschema import validate, ValidationError


@pytest.fixture
def schema():
    """Load the schedule schema."""
    schema_path = Path("dash/schemas/schedule.schema.json")
    return json.loads(schema_path.read_text())


@pytest.fixture
def valid_schedule():
    """A minimal valid schedule."""
    return {
        "schema_version": "0.1",
        "product_id": "test-product",
        "cadence": "daily",
        "jobs": [
            {
                "intent": "validate",
                "budget": {"max_actions": 1},
                "priority": 80
            }
        ],
        "enabled": True
    }


class TestScheduleSchema:
    """Tests for schedule schema."""

    def test_schema_file_exists(self):
        """Schema file should exist."""
        assert Path("dash/schemas/schedule.schema.json").exists()

    def test_schema_is_valid_json(self, schema):
        """Schema should be valid JSON."""
        assert "$schema" in schema
        assert schema["$id"] == "schedule.schema.json"

    def test_valid_schedule_passes(self, schema, valid_schedule):
        """Valid schedule should pass validation."""
        validate(instance=valid_schedule, schema=schema)

    def test_missing_product_id_fails(self, schema, valid_schedule):
        """Missing product_id should fail."""
        del valid_schedule["product_id"]
        with pytest.raises(ValidationError):
            validate(instance=valid_schedule, schema=schema)

    def test_missing_jobs_fails(self, schema, valid_schedule):
        """Missing jobs should fail."""
        del valid_schedule["jobs"]
        with pytest.raises(ValidationError):
            validate(instance=valid_schedule, schema=schema)

    def test_empty_jobs_fails(self, schema, valid_schedule):
        """Empty jobs array should fail."""
        valid_schedule["jobs"] = []
        with pytest.raises(ValidationError):
            validate(instance=valid_schedule, schema=schema)

    def test_invalid_cadence_fails(self, schema, valid_schedule):
        """Invalid cadence should fail."""
        valid_schedule["cadence"] = "every_minute"
        with pytest.raises(ValidationError):
            validate(instance=valid_schedule, schema=schema)

    def test_valid_cadences(self, schema, valid_schedule):
        """All valid cadences should pass."""
        for cadence in ["hourly", "daily", "weekly", "manual", "on_push"]:
            valid_schedule["cadence"] = cadence
            validate(instance=valid_schedule, schema=schema)

    def test_gc_runs_intent(self, schema, valid_schedule):
        """gc_runs intent should be valid."""
        valid_schedule["jobs"][0]["intent"] = "gc_runs"
        validate(instance=valid_schedule, schema=schema)

    def test_drift_check_intent(self, schema, valid_schedule):
        """drift_check intent should be valid."""
        valid_schedule["jobs"][0]["intent"] = "drift_check"
        validate(instance=valid_schedule, schema=schema)


class TestExampleSchedule:
    """Tests for the example schedule file."""

    def test_example_exists(self):
        """Example schedule should exist."""
        assert Path("dash/schedules/codemonkeys-cli.json").exists()

    def test_example_validates(self, schema):
        """Example schedule should validate."""
        path = Path("dash/schedules/codemonkeys-cli.json")
        schedule = json.loads(path.read_text())
        validate(instance=schedule, schema=schema)

    def test_example_has_multiple_jobs(self):
        """Example should have multiple job types."""
        path = Path("dash/schedules/codemonkeys-cli.json")
        schedule = json.loads(path.read_text())
        intents = [job["intent"] for job in schedule["jobs"]]
        assert "validate" in intents
        assert "test" in intents
        assert "gc_runs" in intents
