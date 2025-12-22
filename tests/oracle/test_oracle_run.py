"""Tests for Oracle executor - budget enforcement, stop conditions, dry-run safety."""
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# Import executor functions
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))
from oracle_executor import (
    load_work_orders,
    execute_work_order,
    should_stop,
    run as executor_run,
)


@pytest.fixture
def temp_work_orders_dir():
    """Create a temporary work orders directory with test orders."""
    with tempfile.TemporaryDirectory() as tmpdir:
        wo_dir = Path(tmpdir)
        
        # Create 3 work orders with different priorities
        work_orders = [
            {
                "job_id": "wo_test_validate_001",
                "product_id": "test-product",
                "intent": "validate",
                "inputs": {},
                "budget": {"max_actions": 1},
                "stop_conditions": ["on_silverback_fail"],
                "priority": 100,
                "created_at": "2025-12-22T12:00:00Z",
                "constitution_refs": ["constitution.md"],
                "evidence_expectations": [],
                "status": "pending"
            },
            {
                "job_id": "wo_test_test_002",
                "product_id": "test-product",
                "intent": "test",
                "inputs": {},
                "budget": {"max_actions": 1},
                "stop_conditions": ["on_test_fail"],
                "priority": 50,
                "created_at": "2025-12-22T12:00:00Z",
                "constitution_refs": ["constitution.md"],
                "evidence_expectations": [],
                "status": "pending"
            },
            {
                "job_id": "wo_test_validate_003",
                "product_id": "another-product",
                "intent": "validate",
                "inputs": {},
                "budget": {"max_actions": 1},
                "stop_conditions": [],
                "priority": 10,
                "created_at": "2025-12-22T12:00:00Z",
                "constitution_refs": ["constitution.md"],
                "evidence_expectations": [],
                "status": "pending"
            },
        ]
        
        for wo in work_orders:
            filepath = wo_dir / f"{wo['job_id']}.json"
            with open(filepath, "w") as f:
                json.dump(wo, f)
        
        yield wo_dir


class TestLoadWorkOrders:
    """Tests for work order loading."""

    def test_load_respects_budget(self, temp_work_orders_dir):
        """Load should only return up to budget work orders."""
        result = load_work_orders(temp_work_orders_dir, budget=2)
        assert len(result) == 2

    def test_load_sorts_by_priority(self, temp_work_orders_dir):
        """Loaded work orders should be sorted by priority descending."""
        result = load_work_orders(temp_work_orders_dir, budget=3)
        priorities = [wo["priority"] for wo in result]
        assert priorities == sorted(priorities, reverse=True)

    def test_load_only_pending(self, temp_work_orders_dir):
        """Should only load pending work orders."""
        # Mark one as completed
        completed_file = temp_work_orders_dir / "wo_test_validate_001.json"
        with open(completed_file) as f:
            wo = json.load(f)
        wo["status"] = "completed"
        with open(completed_file, "w") as f:
            json.dump(wo, f)
        
        result = load_work_orders(temp_work_orders_dir, budget=3)
        assert len(result) == 2
        assert all(wo["status"] == "pending" for wo in result)


class TestBudgetEnforcement:
    """Tests for budget enforcement during execution."""

    def test_budget_limits_execution(self, temp_work_orders_dir):
        """Executor should stop after budget is exhausted."""
        with patch("oracle_executor.execute_validate") as mock_validate:
            mock_validate.return_value = (0, "OK")
            
            exit_code = executor_run(
                work_orders_dir=temp_work_orders_dir,
                budget=1,
                dry_run=True
            )
            
            assert exit_code == 0


class TestStopConditions:
    """Tests for stop condition handling."""

    def test_should_stop_on_test_fail(self):
        """Should stop when test fails and on_test_fail is set."""
        wo = {
            "intent": "test",
            "stop_conditions": ["on_test_fail"]
        }
        result = {"status": "failed", "result": {"exit_code": 1}}
        
        stop, reason = should_stop(wo, result)
        assert stop is True
        assert "on_test_fail" in reason

    def test_should_stop_on_silverback_fail(self):
        """Should stop when silverback fails and on_silverback_fail is set."""
        wo = {
            "intent": "validate",
            "stop_conditions": ["on_silverback_fail"]
        }
        result = {"status": "failed", "result": {"exit_code": 1}}
        
        stop, reason = should_stop(wo, result)
        assert stop is True
        assert "on_silverback_fail" in reason

    def test_should_not_stop_without_condition(self):
        """Should not stop if stop condition not in list."""
        wo = {
            "intent": "validate",
            "stop_conditions": []
        }
        result = {"status": "failed", "result": {"exit_code": 1}}
        
        stop, reason = should_stop(wo, result)
        assert stop is False

    def test_should_not_stop_on_success(self):
        """Should not stop on successful execution."""
        wo = {
            "intent": "validate",
            "stop_conditions": ["on_silverback_fail"]
        }
        result = {"status": "completed", "result": {"exit_code": 0}}
        
        stop, reason = should_stop(wo, result)
        assert stop is False


class TestDryRunSafety:
    """Tests for dry-run mode safety."""

    def test_dry_run_does_not_modify_files(self, temp_work_orders_dir):
        """Dry run should not modify work order files."""
        # Get original content
        original_contents = {}
        for f in temp_work_orders_dir.glob("*.json"):
            original_contents[f.name] = f.read_text()
        
        # Run in dry-run mode
        executor_run(
            work_orders_dir=temp_work_orders_dir,
            budget=3,
            dry_run=True
        )
        
        # Check files unchanged
        for f in temp_work_orders_dir.glob("*.json"):
            assert f.read_text() == original_contents[f.name], \
                f"Dry run modified {f.name}"

    def test_dry_run_returns_success(self, temp_work_orders_dir):
        """Dry run should return 0 exit code."""
        exit_code = executor_run(
            work_orders_dir=temp_work_orders_dir,
            budget=1,
            dry_run=True
        )
        assert exit_code == 0


class TestRealExecution:
    """Tests for real (non-dry-run) execution."""

    def test_execute_validate_updates_status(self, temp_work_orders_dir):
        """Real execution should update work order status."""
        with patch("oracle_executor.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="OK", stderr="")
            
            executor_run(
                work_orders_dir=temp_work_orders_dir,
                budget=1,
                dry_run=False
            )
            
            # Check that the file was updated
            wo_file = temp_work_orders_dir / "wo_test_validate_001.json"
            with open(wo_file) as f:
                wo = json.load(f)
            
            assert wo["status"] in ["completed", "failed"]
