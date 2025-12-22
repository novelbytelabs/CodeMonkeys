"""Tests for Oracle planner - determinism and bounded output."""
import json
import tempfile
from pathlib import Path

import pytest

# Import planner functions
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))
from oracle_planner import plan, load_products, calculate_priority


@pytest.fixture
def temp_dash_dir():
    """Create a temporary dash directory with test products."""
    with tempfile.TemporaryDirectory() as tmpdir:
        dash_dir = Path(tmpdir)
        
        # Create products.json
        products = {
            "products": [
                {"product_id": "product-a", "name": "Product A"},
                {"product_id": "product-b", "name": "Product B"},
                {"product_id": "product-c", "name": "Product C"},
                {"product_id": "product-d", "name": "Product D"},
            ]
        }
        products_file = dash_dir / "products.json"
        with open(products_file, "w") as f:
            json.dump(products, f)
        
        # Create runs directory
        runs_dir = dash_dir / "runs"
        runs_dir.mkdir()
        
        # Product A: missing evidence (no last_run.json) -> highest priority
        
        # Product B: failed tests -> high priority
        (runs_dir / "product-b").mkdir()
        with open(runs_dir / "product-b" / "last_run.json", "w") as f:
            json.dump({"status": "failed", "created_at": "2025-12-20T10:00:00Z"}, f)
        
        # Product C: passed -> low priority
        (runs_dir / "product-c").mkdir()
        with open(runs_dir / "product-c" / "last_run.json", "w") as f:
            json.dump({"status": "passed", "created_at": "2025-12-22T10:00:00Z"}, f)
        
        # Product D: governance failed -> very high priority
        (runs_dir / "product-d").mkdir()
        with open(runs_dir / "product-d" / "last_run.json", "w") as f:
            json.dump({"status": "governance_failed", "created_at": "2025-12-21T10:00:00Z"}, f)
        
        yield dash_dir


class TestOraclePlanDeterminism:
    """Tests for deterministic planning."""

    def test_plan_produces_deterministic_order(self, temp_dash_dir):
        """Same inputs should produce same ordered output."""
        products_path = temp_dash_dir / "products.json"
        runs_dir = temp_dash_dir / "runs"
        
        # Run plan twice
        result1 = plan(products_path, runs_dir, budget=4, deterministic=True)
        result2 = plan(products_path, runs_dir, budget=4, deterministic=True)
        
        # Extract just the order-relevant fields
        order1 = [(wo["product_id"], wo["intent"]) for wo in result1]
        order2 = [(wo["product_id"], wo["intent"]) for wo in result2]
        
        assert order1 == order2, "Plan should be deterministic"

    def test_plan_respects_budget(self, temp_dash_dir):
        """Plan should never emit more than budget work orders."""
        products_path = temp_dash_dir / "products.json"
        runs_dir = temp_dash_dir / "runs"
        
        for budget in [1, 2, 3]:
            result = plan(products_path, runs_dir, budget=budget)
            assert len(result) <= budget, f"Budget {budget} violated: got {len(result)}"

    def test_plan_priority_order(self, temp_dash_dir):
        """Higher priority items should come first."""
        products_path = temp_dash_dir / "products.json"
        runs_dir = temp_dash_dir / "runs"
        
        result = plan(products_path, runs_dir, budget=4, deterministic=True)
        priorities = [wo["priority"] for wo in result]
        
        # Should be sorted descending
        assert priorities == sorted(priorities, reverse=True), \
            f"Priorities not in descending order: {priorities}"

    def test_missing_evidence_ranked_highest(self, temp_dash_dir):
        """Products with missing evidence should rank first."""
        products_path = temp_dash_dir / "products.json"
        runs_dir = temp_dash_dir / "runs"
        
        result = plan(products_path, runs_dir, budget=4, deterministic=True)
        
        # Product A has no last_run.json, should be first
        first_product = result[0]["product_id"]
        first_intent = result[0]["intent"]
        
        assert first_product == "product-a", f"Expected product-a first, got {first_product}"
        assert first_intent == "regenerate_report", f"Expected regenerate_report, got {first_intent}"


class TestCalculatePriority:
    """Tests for priority calculation."""

    def test_missing_run_is_highest_priority(self):
        """Missing last_run should return highest priority."""
        priority, intent = calculate_priority({}, None)
        assert priority == 100
        assert intent == "regenerate_report"

    def test_failed_status_high_priority(self):
        """Failed status should be high priority."""
        priority, intent = calculate_priority({}, {"status": "failed"})
        assert priority >= 80
        assert intent == "test"

    def test_governance_failed_highest(self):
        """Governance failure should be very high priority."""
        priority, intent = calculate_priority({}, {"status": "governance_failed"})
        assert priority >= 90
        assert intent == "validate"

    def test_passed_low_priority(self):
        """Passed status should be low priority."""
        priority, intent = calculate_priority({}, {"status": "passed"})
        assert priority <= 20
        assert intent == "validate"
