"""Integration tests for Oracle plan → run workflow.

Self-contained tests that simulate the full loop in a temp workspace.
"""
import json
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))
from oracle_planner import plan, plan_from_schedules, generate_work_order
from oracle_executor import run as executor_run, load_work_orders


@pytest.fixture
def minimal_workspace(tmp_path):
    """Create a minimal workspace with products, schedules, and schemas."""
    # Create directory structure
    dash_dir = tmp_path / "dash"
    runs_dir = dash_dir / "runs"
    schedules_dir = dash_dir / "schedules"
    schemas_dir = dash_dir / "schemas"
    work_orders_dir = tmp_path / "nexus" / "work_orders"

    for d in [runs_dir, schedules_dir, schemas_dir, work_orders_dir]:
        d.mkdir(parents=True)

    # Create products.json
    products = {
        "schema_version": "0.1",
        "products": [
            {
                "product_id": "test-product",
                "display_name": "Test Product",
                "status": "development",
                "enabled": True
            }
        ]
    }
    (dash_dir / "products.json").write_text(json.dumps(products))

    # Create schedule
    schedule = {
        "product_id": "test-product",
        "enabled": True,
        "jobs": [
            {
                "intent": "validate",
                "priority": 90,
                "budget": {"max_actions": 1}
            }
        ]
    }
    (schedules_dir / "test-product.json").write_text(json.dumps(schedule))

    # Create minimal schema
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["schema_version", "product_id"],
        "properties": {
            "schema_version": {"type": "string"},
            "product_id": {"type": "string"}
        }
    }
    (schemas_dir / "last_run.schema.json").write_text(json.dumps(schema))

    return {
        "root": tmp_path,
        "dash": dash_dir,
        "runs": runs_dir,
        "schedules": schedules_dir,
        "work_orders": work_orders_dir,
        "products_path": dash_dir / "products.json"
    }


class TestOraclePlanToRun:
    """Full plan → run integration tests."""

    def test_plan_creates_work_order(self, minimal_workspace):
        """Plan should create work order for product without last_run."""
        work_orders = plan(
            products_path=minimal_workspace["products_path"],
            runs_dir=minimal_workspace["runs"],
            budget=1,
            deterministic=True
        )

        assert len(work_orders) == 1
        wo = work_orders[0]
        assert wo["product_id"] == "test-product"
        assert wo["status"] == "pending"
        # Product without last_run gets regenerate_report intent
        assert wo["intent"] == "regenerate_report"

    def test_plan_from_schedules_creates_work_order(self, minimal_workspace):
        """Plan from schedules should create work order based on schedule."""
        work_orders = plan_from_schedules(
            schedules_dir=minimal_workspace["schedules"],
            budget=1,
            deterministic=True
        )

        assert len(work_orders) == 1
        wo = work_orders[0]
        assert wo["product_id"] == "test-product"
        assert wo["intent"] == "validate"
        assert wo["priority"] == 90

    def test_dry_run_does_not_modify_work_order(self, minimal_workspace):
        """Dry run should not change work order status."""
        # Create a work order file
        wo = generate_work_order(
            product_id="test-product",
            intent="validate",
            priority=50,
            rank=1,
            deterministic=True
        )
        wo_path = minimal_workspace["work_orders"] / f"{wo['job_id']}.json"
        wo_path.write_text(json.dumps(wo))

        # Run in dry-run mode
        exit_code = executor_run(
            work_orders_dir=minimal_workspace["work_orders"],
            budget=1,
            dry_run=True
        )

        assert exit_code == 0

        # Verify work order unchanged
        with open(wo_path) as f:
            after = json.load(f)
        assert after["status"] == "pending"

    def test_real_run_updates_work_order_status(self, minimal_workspace):
        """Real run should update work order status to completed/failed."""
        # Create a work order
        wo = generate_work_order(
            product_id="test-product",
            intent="validate",
            priority=50,
            rank=1,
            deterministic=True
        )
        wo_path = minimal_workspace["work_orders"] / f"{wo['job_id']}.json"
        wo_path.write_text(json.dumps(wo))

        # Mock the actual execution
        with patch("oracle_executor.execute_validate") as mock_validate:
            mock_validate.return_value = (0, "OK")

            exit_code = executor_run(
                work_orders_dir=minimal_workspace["work_orders"],
                budget=1,
                dry_run=False
            )

        assert exit_code == 0

        # Verify work order updated
        with open(wo_path) as f:
            after = json.load(f)
        assert after["status"] == "completed"

    def test_full_loop_plan_then_run(self, minimal_workspace):
        """Full loop: plan creates work order, run executes it."""
        # Step 1: Plan
        work_orders = plan_from_schedules(
            schedules_dir=minimal_workspace["schedules"],
            budget=1,
            deterministic=True
        )
        assert len(work_orders) == 1

        # Write work order to file
        wo = work_orders[0]
        wo_path = minimal_workspace["work_orders"] / f"{wo['job_id']}.json"
        wo_path.write_text(json.dumps(wo))

        # Step 2: Dry run (should not change status)
        exit_code = executor_run(
            work_orders_dir=minimal_workspace["work_orders"],
            budget=1,
            dry_run=True
        )
        assert exit_code == 0

        with open(wo_path) as f:
            after_dry = json.load(f)
        assert after_dry["status"] == "pending", "Dry run should not change status"

        # Step 3: Real run
        with patch("oracle_executor.execute_validate") as mock_validate:
            mock_validate.return_value = (0, "Validation passed")

            exit_code = executor_run(
                work_orders_dir=minimal_workspace["work_orders"],
                budget=1,
                dry_run=False
            )

        assert exit_code == 0

        with open(wo_path) as f:
            after_real = json.load(f)
        assert after_real["status"] == "completed"


class TestLoadWorkOrders:
    """Tests for work order loading."""

    def test_load_respects_budget(self, minimal_workspace):
        """Should only load up to budget work orders."""
        # Create 3 work orders
        for i in range(3):
            wo = generate_work_order(
                product_id=f"product-{i}",
                intent="validate",
                priority=50 + i,
                rank=i,
                deterministic=True
            )
            wo_path = minimal_workspace["work_orders"] / f"{wo['job_id']}.json"
            wo_path.write_text(json.dumps(wo))

        loaded = load_work_orders(minimal_workspace["work_orders"], budget=2)
        assert len(loaded) == 2

    def test_load_sorts_by_priority(self, minimal_workspace):
        """Should load work orders sorted by priority descending."""
        priorities = [10, 90, 50]
        for i, p in enumerate(priorities):
            wo = generate_work_order(
                product_id=f"product-{i}",
                intent="validate",
                priority=p,
                rank=i,
                deterministic=True
            )
            wo_path = minimal_workspace["work_orders"] / f"{wo['job_id']}.json"
            wo_path.write_text(json.dumps(wo))

        loaded = load_work_orders(minimal_workspace["work_orders"], budget=3)
        loaded_priorities = [wo["priority"] for wo in loaded]
        assert loaded_priorities == sorted(loaded_priorities, reverse=True)

    def test_load_skips_completed(self, minimal_workspace):
        """Should only load pending work orders."""
        # Create pending work order
        wo_pending = generate_work_order(
            product_id="pending-product",
            intent="validate",
            priority=50,
            rank=1,
            deterministic=True
        )
        (minimal_workspace["work_orders"] / f"{wo_pending['job_id']}.json").write_text(
            json.dumps(wo_pending)
        )

        # Create completed work order
        wo_completed = generate_work_order(
            product_id="completed-product",
            intent="validate",
            priority=100,
            rank=2,
            deterministic=True
        )
        wo_completed["status"] = "completed"
        (minimal_workspace["work_orders"] / f"{wo_completed['job_id']}.json").write_text(
            json.dumps(wo_completed)
        )

        loaded = load_work_orders(minimal_workspace["work_orders"], budget=2)
        assert len(loaded) == 1
        assert loaded[0]["product_id"] == "pending-product"
