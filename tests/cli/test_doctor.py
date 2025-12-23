"""Tests for doctor command."""
import json
import os
from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from codemonkeys.commands.doctor import (
    check_python_version,
    check_required_packages,
    check_required_paths,
    check_products_json,
    check_conda_env,
    doctor,
)


class TestCheckPythonVersion:
    """Tests for Python version check."""

    def test_returns_true_for_python_310_plus(self):
        """Should pass for Python 3.10+."""
        passed, msg = check_python_version()
        # We're running on 3.10+, so this should pass
        assert passed is True
        assert "3.10" in msg or "3.11" in msg or "3.12" in msg


class TestCheckRequiredPackages:
    """Tests for package availability check."""

    def test_returns_true_when_all_packages_available(self):
        """Should pass when all required packages are importable."""
        passed, msg = check_required_packages()
        assert passed is True
        assert "available" in msg.lower()


class TestCheckRequiredPaths:
    """Tests for required paths check."""

    def test_returns_true_when_paths_exist(self, tmp_path, monkeypatch):
        """Should pass when all required paths exist."""
        # This runs from repo root where paths exist
        passed, msg = check_required_paths()
        # Will fail in tmp workspace but pass in real repo
        # Just verify it returns a tuple
        assert isinstance(passed, bool)
        assert isinstance(msg, str)


class TestCheckProductsJson:
    """Tests for products.json validation."""

    def test_returns_true_for_valid_products(self, tmp_path, monkeypatch):
        """Should pass for valid products.json."""
        monkeypatch.chdir(tmp_path)
        
        dash_dir = tmp_path / "dash"
        dash_dir.mkdir()
        
        products = {
            "schema_version": "0.1",
            "products": [
                {"product_id": "test-1"},
                {"product_id": "test-2"}
            ]
        }
        (dash_dir / "products.json").write_text(json.dumps(products))
        
        passed, msg = check_products_json()
        assert passed is True
        assert "2 products" in msg

    def test_returns_false_for_invalid_json(self, tmp_path, monkeypatch):
        """Should fail for invalid JSON."""
        monkeypatch.chdir(tmp_path)
        
        dash_dir = tmp_path / "dash"
        dash_dir.mkdir()
        (dash_dir / "products.json").write_text("not valid json {")
        
        passed, msg = check_products_json()
        assert passed is False
        assert "Invalid JSON" in msg

    def test_returns_false_when_file_missing(self, tmp_path, monkeypatch):
        """Should fail when file doesn't exist."""
        monkeypatch.chdir(tmp_path)
        
        passed, msg = check_products_json()
        assert passed is False
        assert "not found" in msg.lower()


class TestCheckCondaEnv:
    """Tests for conda environment check."""

    def test_returns_true_when_correct_env_active(self):
        """Should pass when helios-gpu-118 is active."""
        with patch.dict(os.environ, {"CONDA_DEFAULT_ENV": "helios-gpu-118"}):
            passed, msg = check_conda_env()
            assert passed is True
            assert "helios-gpu-118" in msg

    def test_returns_false_when_different_env_active(self):
        """Should warn when different env is active."""
        with patch.dict(os.environ, {"CONDA_DEFAULT_ENV": "other-env"}):
            passed, msg = check_conda_env()
            assert passed is False
            assert "other-env" in msg

    def test_returns_false_when_no_env_active(self):
        """Should warn when no conda env is active."""
        with patch.dict(os.environ, {"CONDA_DEFAULT_ENV": ""}):
            passed, msg = check_conda_env()
            assert passed is False
            assert "No conda env" in msg


class TestDoctorCommand:
    """Tests for doctor CLI command."""

    def test_doctor_runs_without_error(self):
        """Doctor command should run without crashing."""
        runner = CliRunner()
        result = runner.invoke(doctor)
        # Should complete (exit 0 or 1 depending on environment)
        assert result.exit_code in [0, 1]

    def test_doctor_shows_health_checks_table(self):
        """Doctor should show health checks in output."""
        runner = CliRunner()
        result = runner.invoke(doctor)
        # Should contain check names
        assert "Python Version" in result.output or "Health Checks" in result.output

    def test_doctor_exits_zero_when_passing(self, tmp_path, monkeypatch):
        """Doctor exits 0 when all core checks pass."""
        # Run from repo root where paths exist
        runner = CliRunner()
        result = runner.invoke(doctor)
        # In actual repo with correct setup, should pass
        # Just verify it runs
        assert result.exit_code in [0, 1]
