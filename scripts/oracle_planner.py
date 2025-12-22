#!/usr/bin/env python3
"""
Oracle Planner - generates bounded, prioritized work orders.

Reads:
- dash/products.json
- dash/runs/<product_id>/last_run.json

Outputs:
- Work orders as JSON to nexus/work_orders/ or stdout

Usage:
    python scripts/oracle_planner.py --budget 3
    python scripts/oracle_planner.py --budget 3 --stdout
    python scripts/oracle_planner.py --budget 3 --output-dir /tmp/wo
"""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def load_products(products_path: Path) -> list[dict]:
    """Load products from products.json."""
    if not products_path.exists():
        return []
    with open(products_path) as f:
        data = json.load(f)
    return data.get("products", [])


def load_last_run(product_id: str, runs_dir: Path) -> dict | None:
    """Load last run for a product if it exists."""
    run_file = runs_dir / product_id / "last_run.json"
    if not run_file.exists():
        return None
    with open(run_file) as f:
        return json.load(f)


def calculate_priority(product: dict, last_run: dict | None) -> tuple[int, str]:
    """
    Calculate priority score for a product.
    
    Returns (priority_score, recommended_intent).
    Higher score = more urgent.
    """
    # Default: low priority validate
    priority = 0
    intent = "validate"
    
    if last_run is None:
        # Missing run = needs report generation
        return (100, "regenerate_report")
    
    status = last_run.get("status", "unknown")
    
    if status == "failed":
        # Failed tests = high priority
        priority = 80
        intent = "test"
    elif status == "governance_failed":
        # Governance failure = highest priority
        priority = 90
        intent = "validate"
    elif status == "passed":
        # Passed = low priority, just validate
        priority = 10
        intent = "validate"
    else:
        # Unknown status = medium priority
        priority = 50
        intent = "validate"
    
    # Boost priority for stale runs (older than 1 day conceptually)
    created = last_run.get("created_at", "")
    if created:
        # Simple staleness check (placeholder for actual time comparison)
        priority += 5
    
    return (priority, intent)


def generate_work_order(
    product_id: str,
    intent: str,
    priority: int,
    rank: int,
    deterministic: bool = False
) -> dict[str, Any]:
    """Generate a single work order."""
    if deterministic:
        job_id = f"wo_{product_id}_{intent}_{rank:03d}"
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        job_id = f"wo_{product_id}_{intent}_{timestamp}_{rank:03d}"
    
    # Define inputs based on intent
    inputs: dict[str, Any] = {}
    if intent == "regenerate_report":
        inputs["product_id"] = product_id
    
    # Define evidence expectations
    evidence = [f"dash/runs/{product_id}/last_run.json"]
    
    return {
        "job_id": job_id,
        "product_id": product_id,
        "intent": intent,
        "inputs": inputs,
        "budget": {"max_actions": 1, "max_seconds": 120},
        "stop_conditions": ["on_silverback_fail", "on_test_fail", "on_missing_evidence"],
        "priority": priority,
        "created_at": datetime.now().isoformat() + "Z",
        "constitution_refs": ["constitution.md"],
        "evidence_expectations": evidence,
        "status": "pending"
    }


def plan(
    products_path: Path,
    runs_dir: Path,
    budget: int,
    deterministic: bool = False
) -> list[dict]:
    """
    Generate bounded, prioritized work orders.
    
    Returns up to `budget` work orders, sorted by priority (descending).
    """
    products = load_products(products_path)
    
    # Calculate priority for each product
    scored_products = []
    for product in products:
        product_id = product.get("product_id")
        if not product_id:
            continue
        last_run = load_last_run(product_id, runs_dir)
        priority, intent = calculate_priority(product, last_run)
        scored_products.append({
            "product_id": product_id,
            "priority": priority,
            "intent": intent
        })
    
    # Sort by priority (descending), then by product_id (stable sort)
    scored_products.sort(key=lambda x: (-x["priority"], x["product_id"]))
    
    # Generate work orders for top N
    work_orders = []
    for rank, sp in enumerate(scored_products[:budget], start=1):
        wo = generate_work_order(
            product_id=sp["product_id"],
            intent=sp["intent"],
            priority=sp["priority"],
            rank=rank,
            deterministic=deterministic
        )
        work_orders.append(wo)
    
    return work_orders


def main():
    parser = argparse.ArgumentParser(description="Oracle Planner")
    parser.add_argument("--budget", type=int, default=3, help="Max work orders to generate")
    parser.add_argument("--stdout", action="store_true", help="Output to stdout instead of files")
    parser.add_argument("--output-dir", type=Path, default=Path("nexus/work_orders"), help="Output directory")
    parser.add_argument("--products", type=Path, default=Path("dash/products.json"), help="Products file")
    parser.add_argument("--runs-dir", type=Path, default=Path("dash/runs"), help="Runs directory")
    parser.add_argument("--deterministic", action="store_true", help="Use deterministic job IDs")
    
    args = parser.parse_args()
    
    work_orders = plan(
        products_path=args.products,
        runs_dir=args.runs_dir,
        budget=args.budget,
        deterministic=args.deterministic
    )
    
    if not work_orders:
        print("No work orders generated (no products found).", file=sys.stderr)
        return 0
    
    if args.stdout:
        print(json.dumps(work_orders, indent=2))
    else:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        for wo in work_orders:
            filename = f"{wo['job_id']}.json"
            filepath = args.output_dir / filename
            with open(filepath, "w") as f:
                json.dump(wo, f, indent=2)
            print(f"Created: {filepath}")
    
    print(f"\n✅ Generated {len(work_orders)} work order(s)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
