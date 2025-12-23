"""Tests for products registry schema and multi-product planning."""
import json
from pathlib import Path

import pytest
from jsonschema import validate, ValidationError


@pytest.fixture
def schema():
    """Load the products schema."""
    schema_path = Path("dash/schemas/products.schema.json")
    return json.loads(schema_path.read_text())


@pytest.fixture
def products():
    """Load the products registry."""
    products_path = Path("dash/products.json")
    return json.loads(products_path.read_text())


class TestProductsSchema:
    """Tests for products registry schema."""

    def test_schema_file_exists(self):
        """Schema file should exist."""
        assert Path("dash/schemas/products.schema.json").exists()

    def test_products_file_exists(self):
        """Products file should exist."""
        assert Path("dash/products.json").exists()

    def test_products_validates(self, schema, products):
        """Products should validate against schema."""
        validate(instance=products, schema=schema)

    def test_has_multiple_products(self, products):
        """Should have 3+ products."""
        assert len(products["products"]) >= 3

    def test_products_have_owner(self, products):
        """All products should have owner."""
        for product in products["products"]:
            assert "owner" in product
            assert product["owner"]

    def test_high_criticality_products_exist(self, products):
        """Should have high criticality products."""
        high_crit = [p for p in products["products"]
                     if p.get("criticality") == "high"]
        assert len(high_crit) >= 1


class TestMultiProductSchedules:
    """Tests for multi-product schedules."""

    def test_schedule_files_exist(self):
        """Multiple schedule files should exist."""
        schedule_dir = Path("dash/schedules")
        schedules = list(schedule_dir.glob("*.json"))
        assert len(schedules) >= 3

    def test_schedules_have_distinct_products(self):
        """Schedules should be for different products."""
        schedule_dir = Path("dash/schedules")
        product_ids = set()

        for schedule_file in schedule_dir.glob("*.json"):
            schedule = json.loads(schedule_file.read_text())
            product_ids.add(schedule.get("product_id"))

        assert len(product_ids) >= 3

    def test_enabled_schedules(self):
        """At least some schedules should be enabled."""
        schedule_dir = Path("dash/schedules")
        enabled_count = 0

        for schedule_file in schedule_dir.glob("*.json"):
            schedule = json.loads(schedule_file.read_text())
            if schedule.get("enabled", False):
                enabled_count += 1

        assert enabled_count >= 2
