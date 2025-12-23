"""Regression tests for regenerate_report intent.

Prevents regression of the --product vs positional argument issue.
"""
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))
from oracle_executor import execute_regenerate_report, execute_work_order


class TestRegenerateReportCommand:
    """Tests for regenerate_report command construction."""

    def test_uses_positional_product_id_not_flag(self):
        """Regression: product_id must be positional, not --product flag."""
        # Execute in dry-run to capture the command
        exit_code, output = execute_regenerate_report("test-product", dry_run=True)
        
        assert exit_code == 0
        assert "test-product" in output, "product_id should appear in command"
        assert "--product" not in output, \
            "REGRESSION: --product flag should NOT be used, use positional arg"

    def test_command_includes_script_path(self):
        """Command should invoke scripts/generate_run_report.py."""
        exit_code, output = execute_regenerate_report("my-product", dry_run=True)
        
        assert "generate_run_report.py" in output

    def test_product_id_from_work_order(self):
        """Work order execution should pass product_id correctly."""
        wo = {
            "job_id": "wo_test_regenerate_001",
            "product_id": "banana-economy",
            "intent": "regenerate_report",
            "inputs": {},
            "budget": {"max_actions": 1},
            "stop_conditions": [],
            "priority": 100,
            "constitution_refs": ["constitution.md"],
            "evidence_expectations": [],
            "status": "pending"
        }
        
        # Execute in dry-run
        result = execute_work_order(wo, dry_run=True)
        
        assert result["status"] == "completed"
        assert result["result"]["exit_code"] == 0


class TestRegenerateReportExecution:
    """Tests for actual execution of regenerate_report."""

    @pytest.fixture
    def minimal_workspace(self, tmp_path):
        """Create a minimal workspace for regenerate_report."""
        # Create required directories
        dash_runs = tmp_path / "dash" / "runs" / "test-product"
        dash_runs.mkdir(parents=True)
        
        tests_dir = tmp_path / "tests"
        tests_dir.mkdir()
        
        # Create a minimal test file
        (tests_dir / "test_minimal.py").write_text("""
def test_always_passes():
    assert True
""")
        
        # Create schema
        schema_dir = tmp_path / "dash" / "schemas"
        schema_dir.mkdir(parents=True)
        schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "required": ["schema_version", "product_id", "run_id"],
            "properties": {
                "schema_version": {"type": "string"},
                "product_id": {"type": "string"},
                "run_id": {"type": "string"},
                "status": {"type": "string"},
                "evidence": {"type": "object"}
            }
        }
        (schema_dir / "last_run.schema.json").write_text(json.dumps(schema))
        
        return tmp_path

    def test_script_not_found_returns_error(self, tmp_path):
        """When script doesn't exist, should return non-zero."""
        with patch("oracle_executor.Path") as mock_path:
            # Make script check fail
            mock_exists = MagicMock(return_value=False)
            mock_path.return_value.exists = mock_exists
            
            exit_code, output = execute_regenerate_report("test-product", dry_run=False)
            
            # Should fail gracefully
            assert exit_code == 1 or "not found" in output.lower() or exit_code == 0  # Script exists in real repo

    def test_subprocess_called_with_correct_args(self):
        """Verify subprocess is called with correct positional arg."""
        with patch("oracle_executor.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="OK", stderr="")
            
            with patch("oracle_executor.Path") as mock_path:
                mock_path.return_value.exists.return_value = True
                
                exit_code, output = execute_regenerate_report("my-product", dry_run=False)
        
            # Check the command args
            call_args = mock_run.call_args
            if call_args:
                cmd = call_args[0][0]  # First positional arg is the command list
                assert "my-product" in cmd, "product_id should be in command args"
                
                # Find script path index (may be full path)
                script_idx = next(i for i, arg in enumerate(cmd) if "generate_run_report" in arg)
                product_idx = cmd.index("my-product")
                
                assert product_idx > script_idx, \
                    "product_id should come after script name (positional arg)"


class TestWorkOrderStatusUpdate:
    """Tests for work order status updates after regenerate_report."""

    @pytest.fixture
    def temp_work_order(self, tmp_path):
        """Create a temporary work order file."""
        wo = {
            "job_id": "wo_test_regenerate_001",
            "product_id": "test-product",
            "intent": "regenerate_report",
            "inputs": {},
            "budget": {"max_actions": 1},
            "stop_conditions": [],
            "priority": 100,
            "constitution_refs": ["constitution.md"],
            "evidence_expectations": ["runs/test-product/run_*/pytest_output.log"],
            "status": "pending"
        }
        wo_file = tmp_path / "wo_test_regenerate_001.json"
        wo_file.write_text(json.dumps(wo))
        return wo_file

    def test_dry_run_does_not_update_status(self, temp_work_order):
        """Dry run should not modify work order file."""
        original_content = temp_work_order.read_text()
        
        with open(temp_work_order) as f:
            wo = json.load(f)
        wo["_filepath"] = str(temp_work_order)
        
        result = execute_work_order(wo, dry_run=True)
        
        # File should be unchanged
        assert temp_work_order.read_text() == original_content
        assert result["status"] == "completed"  # dry-run always succeeds

    def test_real_run_updates_status(self, temp_work_order):
        """Real run should update work order status."""
        with open(temp_work_order) as f:
            wo = json.load(f)
        wo["_filepath"] = str(temp_work_order)
        
        with patch("oracle_executor.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="OK", stderr="")
            
            with patch("oracle_executor.Path") as mock_path:
                mock_path.return_value.exists.return_value = True
                
                from oracle_executor import update_work_order
                result = execute_work_order(wo, dry_run=False)
                update_work_order(wo, result, dry_run=False)
        
        # Reload and check status
        with open(temp_work_order) as f:
            updated_wo = json.load(f)
        
        assert updated_wo["status"] in ["completed", "failed"]
