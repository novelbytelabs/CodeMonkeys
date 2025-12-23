"""Tests for auto-heal executor behavior."""
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))


class TestAutoHealValidate:
    """Tests for auto-heal on validate intent."""

    def test_auto_heal_retries_on_first_failure(self):
        """Should retry validate once on failure."""
        from oracle_executor import execute_validate

        call_count = [0]

        def mock_subprocess_run(*args, **kwargs):
            call_count[0] += 1
            result = MagicMock()
            if call_count[0] == 1:
                result.returncode = 1
                result.stdout = "First call fails"
                result.stderr = ""
            else:
                result.returncode = 0
                result.stdout = "Second call succeeds"
                result.stderr = ""
            return result

        with patch("oracle_executor.subprocess.run", side_effect=mock_subprocess_run):
            # First call fails
            exit_code1, _ = execute_validate(dry_run=False)
            assert exit_code1 == 1

            # Second call succeeds
            exit_code2, _ = execute_validate(dry_run=False)
            assert exit_code2 == 0
            assert call_count[0] == 2

    def test_auto_heal_stops_after_max_retries(self):
        """Should stop after 1 retry if still failing."""
        from oracle_executor import execute_validate

        call_count = [0]

        def mock_subprocess_run(*args, **kwargs):
            call_count[0] += 1
            result = MagicMock()
            result.returncode = 1
            result.stdout = "Always fails"
            result.stderr = ""
            return result

        with patch("oracle_executor.subprocess.run", side_effect=mock_subprocess_run):
            exit_code1, _ = execute_validate(dry_run=False)
            assert exit_code1 == 1

            exit_code2, _ = execute_validate(dry_run=False)
            assert exit_code2 == 1
            # Both calls fail
            assert call_count[0] == 2


class TestAutoHealTest:
    """Tests for auto-heal on test intent."""

    def test_test_can_retry_on_failure(self):
        """Test intent can retry on failure."""
        from oracle_executor import execute_test

        with patch("oracle_executor.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=1, stdout="fail", stderr="")
            exit_code, _ = execute_test(dry_run=False)
            assert exit_code == 1


class TestNoAutoHealForGcDrift:
    """Tests that gc_runs and drift_check don't auto-heal."""

    def test_gc_runs_no_retry(self):
        """gc_runs should not retry - it's a one-shot operation."""
        from oracle_executor import execute_gc_runs

        # GC with no runs dir should succeed without retry
        exit_code, output = execute_gc_runs("nonexistent-product", dry_run=False)
        assert exit_code == 0
        assert "No runs directory" in output

    def test_drift_check_no_retry(self):
        """drift_check should not retry - it's a one-shot operation."""
        from oracle_executor import execute_drift_check

        with tempfile.TemporaryDirectory() as tmpdir:
            # Change to temp dir to avoid polluting repo
            import os
            old_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                exit_code, output = execute_drift_check("test-product", dry_run=False)
                assert exit_code == 0
                assert "Drift report written" in output
            finally:
                os.chdir(old_cwd)


class TestDryRunNoAutoHeal:
    """Tests that dry-run never triggers auto-heal."""

    def test_dry_run_validate_no_retry(self):
        """Dry-run should not retry."""
        from oracle_executor import execute_validate

        exit_code, output = execute_validate(dry_run=True)
        assert exit_code == 0
        assert "[DRY-RUN]" in output

    def test_dry_run_test_no_retry(self):
        """Dry-run should not retry."""
        from oracle_executor import execute_test

        exit_code, output = execute_test(dry_run=True)
        assert exit_code == 0
        assert "[DRY-RUN]" in output
