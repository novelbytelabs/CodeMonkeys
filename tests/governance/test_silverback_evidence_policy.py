"""Tests for Silverback evidence policy - tiered WARN/ERROR based on product status."""
import json
import tempfile
from pathlib import Path
from unittest.mock import patch
import pytest

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))
from silverback_validate import validate_run_artifact, ValidationResult


@pytest.fixture
def minimal_run_artifact():
    """Factory for creating a minimal run artifact."""
    def _create(product_id: str, evidence_path: str = "runs/test/run_001/pytest_output.log"):
        return {
            "schema_version": "0.1",
            "product_id": product_id,
            "run_id": "run_001",
            "started_at": "2025-01-01T00:00:00Z",
            "ended_at": "2025-01-01T00:01:00Z",
            "status": "success",
            "summary": "All tests passed",
            "evidence": {
                "paths": [evidence_path]
            },
            "banana_economy": {
                "budget_tokens": 50000,
                "spent_tokens": 0,
                "budget_minutes": 90,
                "spent_minutes": 1.0,
                "max_ci_heal_attempts": 2,
                "ci_heal_attempts_used": 0
            },
            "kill_switch": {"enabled": False, "reason": ""},
            "pr_wave": {"state": "none", "open_prs": 0, "last_update": "2025-01-01T00:01:00Z"}
        }
    return _create


@pytest.fixture
def mock_products_registry():
    """Mock products.json registry with active and development products."""
    return {
        "schema_version": "0.1",
        "products": [
            {"product_id": "prod-active", "status": "active"},
            {"product_id": "prod-development", "status": "development"},
            {"product_id": "prod-planned", "status": "planned"},
        ]
    }


class TestEvidencePolicyTiered:
    """Tests for tiered evidence policy based on product status."""

    def test_active_product_missing_evidence_is_error(self, minimal_run_artifact, mock_products_registry, tmp_path):
        """Active (production) products should get ERROR for missing evidence."""
        # Setup: create artifact file in temp dir
        artifact_data = minimal_run_artifact("prod-active")
        artifact_path = tmp_path / "last_run.json"
        artifact_path.write_text(json.dumps(artifact_data))

        # Mock the registry and schema paths
        with patch("silverback_validate.Path") as mock_path_cls:
            # Make Path behave normally but return our mock data for specific paths
            mock_path_cls.side_effect = lambda p: Path(p)
            
            # Create actual test setup in tmp_path
            registry_path = tmp_path / "dash" / "products.json"
            registry_path.parent.mkdir(parents=True, exist_ok=True)
            registry_path.write_text(json.dumps(mock_products_registry))

            # Run validation with patched _get_product_status
            with patch("silverback_validate._get_product_status", return_value="active"):
                with patch("silverback_validate.DASH_SCHEMA_DIR", tmp_path / "schemas"):
                    result = ValidationResult()
                    validate_run_artifact(artifact_path, result)

        # Assert: missing evidence for active product should be ERROR
        assert len(result.errors) >= 1, "Expected at least 1 error for missing evidence"
        assert any("production product" in e for e in result.errors), \
            f"Expected 'production product' in error messages, got: {result.errors}"
        assert len(result.warnings) == 0 or not any("Evidence missing" in w for w in result.warnings), \
            "Should not have warning for missing evidence on active product"

    def test_development_product_missing_evidence_is_warn(self, minimal_run_artifact, mock_products_registry, tmp_path):
        """Development products should get WARN for missing evidence (not ERROR)."""
        # Setup
        artifact_data = minimal_run_artifact("prod-development")
        artifact_path = tmp_path / "last_run.json"
        artifact_path.write_text(json.dumps(artifact_data))

        with patch("silverback_validate._get_product_status", return_value="development"):
            with patch("silverback_validate.DASH_SCHEMA_DIR", tmp_path / "schemas"):
                result = ValidationResult()
                validate_run_artifact(artifact_path, result)

        # Assert: missing evidence for dev product should be WARN only
        evidence_errors = [e for e in result.errors if "Evidence missing" in e]
        assert len(evidence_errors) == 0, \
            f"Expected no errors for missing evidence on dev product, got: {evidence_errors}"
        assert any("dev product" in w for w in result.warnings), \
            f"Expected 'dev product' in warning messages, got: {result.warnings}"

    def test_planned_product_missing_evidence_is_warn(self, minimal_run_artifact, tmp_path):
        """Planned products should also get WARN for missing evidence."""
        artifact_data = minimal_run_artifact("prod-planned")
        artifact_path = tmp_path / "last_run.json"
        artifact_path.write_text(json.dumps(artifact_data))

        with patch("silverback_validate._get_product_status", return_value="planned"):
            with patch("silverback_validate.DASH_SCHEMA_DIR", tmp_path / "schemas"):
                result = ValidationResult()
                validate_run_artifact(artifact_path, result)

        # Assert: WARN not ERROR
        evidence_errors = [e for e in result.errors if "Evidence missing" in e]
        assert len(evidence_errors) == 0, \
            f"Expected no errors for missing evidence on planned product, got: {evidence_errors}"

    def test_unknown_product_missing_evidence_is_warn(self, minimal_run_artifact, tmp_path):
        """Unknown products (not in registry) should default to WARN for missing evidence."""
        artifact_data = minimal_run_artifact("unknown-product")
        artifact_path = tmp_path / "last_run.json"
        artifact_path.write_text(json.dumps(artifact_data))

        with patch("silverback_validate._get_product_status", return_value="unknown"):
            with patch("silverback_validate.DASH_SCHEMA_DIR", tmp_path / "schemas"):
                result = ValidationResult()
                validate_run_artifact(artifact_path, result)

        # Assert: unknown should be treated as non-production (WARN)
        evidence_errors = [e for e in result.errors if "Evidence missing" in e]
        assert len(evidence_errors) == 0, \
            f"Expected no errors for missing evidence on unknown product, got: {evidence_errors}"

    def test_evidence_exists_is_always_ok(self, minimal_run_artifact, tmp_path):
        """When evidence exists, should always be OK regardless of product status."""
        artifact_data = minimal_run_artifact("prod-active", "runs/test/run_001/pytest_output.log")
        artifact_path = tmp_path / "last_run.json"
        artifact_path.write_text(json.dumps(artifact_data))

        # Create the evidence file
        evidence_dir = tmp_path / "dash" / "runs" / "test" / "run_001"
        evidence_dir.mkdir(parents=True, exist_ok=True)
        (evidence_dir / "pytest_output.log").write_text("test output")

        with patch("silverback_validate._get_product_status", return_value="active"):
            with patch("silverback_validate.DASH_SCHEMA_DIR", tmp_path / "schemas"):
                # Patch Path("dash") to use tmp_path/dash
                original_path = Path
                def patched_path(p):
                    if p == "dash":
                        return tmp_path / "dash"
                    return original_path(p)
                
                with patch("silverback_validate.Path", side_effect=patched_path):
                    result = ValidationResult()
                    validate_run_artifact(artifact_path, result)

        # When evidence exists, no errors or warnings about missing evidence
        evidence_errors = [e for e in result.errors if "Evidence missing" in e]
        evidence_warnings = [w for w in result.warnings if "Evidence missing" in w]
        assert len(evidence_errors) == 0
        assert len(evidence_warnings) == 0
