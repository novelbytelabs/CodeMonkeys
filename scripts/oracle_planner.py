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


def find_pending_science_dossiers(science_dir: Path, dossiers_dir: Path) -> list[dict]:
    """Find science dossiers that need conversion to design dossiers."""
    pending = []

    if not science_dir.exists():
        return pending

    for sci_file in science_dir.glob("SCI-*.md"):
        try:
            import frontmatter
            post = frontmatter.load(sci_file)
            meta = post.metadata

            # Only process validated dossiers
            if meta.get("status") != "validated":
                continue

            dossier_id = meta.get("dossier_id", "")
            topic = meta.get("topic", sci_file.stem)

            # Check if design dossier already exists for this science input
            # (By convention: we look for DOS-*-<topic-slug>.md)
            topic_slug = topic.lower().replace(" ", "-")
            existing = list(dossiers_dir.glob(f"DOS-*-{topic_slug}.md"))
            if existing:
                continue

            pending.append({
                "science_path": str(sci_file),
                "dossier_id": dossier_id,
                "topic": topic,
                "priority": 75  # Science intake is high priority
            })
        except Exception:
            continue

    return pending


def generate_science_work_order(
    science_dossier: dict,
    rank: int,
    deterministic: bool = False
) -> dict[str, Any]:
    """Generate a work order to convert science dossier to design dossier."""
    topic_slug = science_dossier["topic"].lower().replace(" ", "-")

    if deterministic:
        job_id = f"wo_science_{topic_slug}_science_to_design_{rank:03d}"
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        job_id = f"wo_science_{topic_slug}_science_to_design_{timestamp}_{rank:03d}"

    return {
        "job_id": job_id,
        "product_id": f"science-{topic_slug}",
        "intent": "science_to_design",
        "inputs": {
            "science_path": science_dossier["science_path"],
            "product_id": topic_slug
        },
        "budget": {"max_actions": 1, "max_seconds": 60},
        "stop_conditions": ["on_validation_fail"],
        "priority": science_dossier["priority"],
        "created_at": datetime.now().isoformat() + "Z",
        "constitution_refs": ["constitution.md"],
        "evidence_expectations": [f"docs/dossiers/DOS-*-{topic_slug}.md"],
        "status": "pending"
    }


def plan_with_science(
    products_path: Path,
    runs_dir: Path,
    science_dir: Path,
    dossiers_dir: Path,
    budget: int,
    deterministic: bool = False
) -> list[dict]:
    """
    Generate bounded, prioritized work orders including science intake.

    Returns up to `budget` work orders, sorted by priority (descending).
    """
    # Get product work orders
    product_wos = plan(products_path, runs_dir, budget, deterministic)

    # Get science intake work orders
    pending_science = find_pending_science_dossiers(science_dir, dossiers_dir)
    science_wos = []
    for rank, sci in enumerate(pending_science, start=len(product_wos) + 1):
        wo = generate_science_work_order(sci, rank, deterministic)
        science_wos.append(wo)

    # Combine and sort by priority
    all_wos = product_wos + science_wos
    all_wos.sort(key=lambda x: -x["priority"])

    return all_wos[:budget]


def load_schedules(schedules_dir: Path, product_filter: str | None = None) -> list[dict]:
    """Load enabled schedules from dash/schedules/."""
    schedules = []

    if not schedules_dir.exists():
        return schedules

    for schedule_file in schedules_dir.glob("*.json"):
        with open(schedule_file) as f:
            schedule = json.load(f)

        if not schedule.get("enabled", False):
            continue

        if product_filter and schedule.get("product_id") != product_filter:
            continue

        schedules.append(schedule)

    return schedules


def plan_from_schedules(
    schedules_dir: Path,
    budget: int,
    product_filter: str | None = None,
    deterministic: bool = False
) -> list[dict]:
    """Generate work orders from schedule definitions."""
    schedules = load_schedules(schedules_dir, product_filter)
    work_orders = []
    rank = 0

    for schedule in schedules:
        product_id = schedule.get("product_id", "unknown")
        jobs = schedule.get("jobs", [])

        for job in jobs:
            if rank >= budget:
                break

            rank += 1
            intent = job.get("intent", "validate")
            priority = job.get("priority", 50)
            job_budget = job.get("budget", {"max_actions": 1})
            stop_conditions = job.get("stop_conditions", [])

            if deterministic:
                job_id = f"wo_{product_id}_{intent}_{rank:03d}"
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                job_id = f"wo_{product_id}_{intent}_{timestamp}_{rank:03d}"

            wo = {
                "job_id": job_id,
                "product_id": product_id,
                "intent": intent,
                "inputs": {"product_id": product_id},
                "budget": job_budget,
                "stop_conditions": stop_conditions,
                "priority": priority,
                "created_at": datetime.now().isoformat() + "Z",
                "constitution_refs": ["constitution.md"],
                "evidence_expectations": [],
                "status": "pending"
            }
            work_orders.append(wo)

        if rank >= budget:
            break

    # Sort by priority descending
    work_orders.sort(key=lambda x: -x["priority"])
    return work_orders[:budget]


def main():
    parser = argparse.ArgumentParser(description="Oracle Planner")
    parser.add_argument("--budget", type=int, default=3, help="Max work orders to generate")
    parser.add_argument("--stdout", action="store_true", help="Output to stdout instead of files")
    parser.add_argument("--output-dir", type=Path, default=Path("nexus/work_orders"), help="Output directory")
    parser.add_argument("--products", type=Path, default=Path("dash/products.json"), help="Products file")
    parser.add_argument("--runs-dir", type=Path, default=Path("dash/runs"), help="Runs directory")
    parser.add_argument("--schedules-dir", type=Path, default=Path("dash/schedules"), help="Schedules directory")
    parser.add_argument("--deterministic", action="store_true", help="Use deterministic job IDs")
    parser.add_argument("--from-schedules", action="store_true", help="Plan from schedule files")
    parser.add_argument("--product", type=str, default=None, help="Filter to single product")

    args = parser.parse_args()

    if args.from_schedules:
        work_orders = plan_from_schedules(
            schedules_dir=args.schedules_dir,
            budget=args.budget,
            product_filter=args.product,
            deterministic=args.deterministic
        )
    else:
        work_orders = plan(
            products_path=args.products,
            runs_dir=args.runs_dir,
            budget=args.budget,
            deterministic=args.deterministic
        )

    if not work_orders:
        print("No work orders generated.", file=sys.stderr)
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

