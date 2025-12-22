"""
Nexus Schema Validation Tests

Validates that nexus/inbox and nexus/outbox artifacts conform to their JSON schemas.
"""
import json
from pathlib import Path

import pytest

try:
    from jsonschema import validate, ValidationError
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False

# Paths
NEXUS_DIR = Path("nexus")
INBOX_DIR = NEXUS_DIR / "inbox"
OUTBOX_DIR = NEXUS_DIR / "outbox"
SCHEMAS_DIR = NEXUS_DIR / "schemas"


@pytest.fixture
def request_schema():
    """Load the Nexus request schema."""
    schema_path = SCHEMAS_DIR / "request.schema.json"
    if not schema_path.exists():
        pytest.skip("Request schema not found")
    return json.loads(schema_path.read_text())


@pytest.fixture
def decision_schema():
    """Load the Nexus decision schema."""
    schema_path = SCHEMAS_DIR / "decision.schema.json"
    if not schema_path.exists():
        pytest.skip("Decision schema not found")
    return json.loads(schema_path.read_text())


def get_inbox_files():
    """Get all JSON files in the inbox directory."""
    if not INBOX_DIR.exists():
        return []
    return list(INBOX_DIR.glob("*.json"))


def get_outbox_files():
    """Get all JSON files in the outbox directory."""
    if not OUTBOX_DIR.exists():
        return []
    return list(OUTBOX_DIR.glob("*.json"))


@pytest.mark.skipif(not HAS_JSONSCHEMA, reason="jsonschema not installed")
class TestNexusInboxSchema:
    """Tests for Nexus inbox (request) artifacts."""

    def test_inbox_files_exist(self):
        """At least one inbox file should exist for testing."""
        files = get_inbox_files()
        assert len(files) > 0, "No inbox files found for validation"

    def test_inbox_files_valid_json(self):
        """All inbox files should be valid JSON."""
        for filepath in get_inbox_files():
            try:
                json.loads(filepath.read_text())
            except json.JSONDecodeError as e:
                pytest.fail(f"Invalid JSON in {filepath}: {e}")

    def test_inbox_files_conform_to_schema(self, request_schema):
        """All inbox files should conform to the request schema."""
        for filepath in get_inbox_files():
            data = json.loads(filepath.read_text())
            try:
                validate(instance=data, schema=request_schema)
            except ValidationError as e:
                pytest.fail(f"Schema validation failed for {filepath}: {e.message}")

    def test_inbox_files_have_required_fields(self):
        """All inbox files should have required fields."""
        required = ["schema_version", "request_id", "type", "source", "created_at", "status", "payload"]
        for filepath in get_inbox_files():
            data = json.loads(filepath.read_text())
            for field in required:
                assert field in data, f"Missing required field '{field}' in {filepath}"


@pytest.mark.skipif(not HAS_JSONSCHEMA, reason="jsonschema not installed")
class TestNexusOutboxSchema:
    """Tests for Nexus outbox (decision) artifacts."""

    def test_outbox_files_exist(self):
        """At least one outbox file should exist for testing."""
        files = get_outbox_files()
        assert len(files) > 0, "No outbox files found for validation"

    def test_outbox_files_valid_json(self):
        """All outbox files should be valid JSON."""
        for filepath in get_outbox_files():
            try:
                json.loads(filepath.read_text())
            except json.JSONDecodeError as e:
                pytest.fail(f"Invalid JSON in {filepath}: {e}")

    def test_outbox_files_conform_to_schema(self, decision_schema):
        """All outbox files should conform to the decision schema."""
        for filepath in get_outbox_files():
            data = json.loads(filepath.read_text())
            try:
                validate(instance=data, schema=decision_schema)
            except ValidationError as e:
                pytest.fail(f"Schema validation failed for {filepath}: {e.message}")

    def test_outbox_files_have_required_fields(self):
        """All outbox files should have required fields."""
        required = ["schema_version", "decision_id", "type", "created_at", "status", "payload"]
        for filepath in get_outbox_files():
            data = json.loads(filepath.read_text())
            for field in required:
                assert field in data, f"Missing required field '{field}' in {filepath}"

    def test_outbox_governance_check_when_present(self):
        """Governance check should be valid when present."""
        for filepath in get_outbox_files():
            data = json.loads(filepath.read_text())
            if "governance_check" in data:
                gc = data["governance_check"]
                assert "compliant" in gc, f"Missing 'compliant' in governance_check of {filepath}"
                assert isinstance(gc["compliant"], bool), f"'compliant' must be boolean in {filepath}"
