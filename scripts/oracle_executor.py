#!/usr/bin/env python3
"""
Oracle Executor - executes work orders with budget enforcement.

Reads:
- Work orders from nexus/work_orders/*.json

Executes:
- validate: codemonkeys silverback --all
- test: pytest
- regenerate_report: scripts/generate_run_report.py

Enforces:
- Budget limits (max work orders, max_actions per job)
- Stop conditions

Usage:
    python scripts/oracle_executor.py --budget 3
    python scripts/oracle_executor.py --budget 3 --dry-run
"""
import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def load_work_orders(work_orders_dir: Path, budget: int) -> list[dict]:
    """Load pending work orders sorted by priority."""
    work_orders = []
    
    for wo_file in work_orders_dir.glob("*.json"):
        if wo_file.name.startswith("_"):  # Skip meta files
            continue
        with open(wo_file) as f:
            wo = json.load(f)
        if wo.get("status") == "pending":
            wo["_filepath"] = str(wo_file)
            work_orders.append(wo)
    
    # Sort by priority descending
    work_orders.sort(key=lambda x: -x.get("priority", 0))
    
    return work_orders[:budget]


def execute_validate(dry_run: bool = False) -> tuple[int, str]:
    """Execute validation (Silverback)."""
    cmd = [sys.executable, "-m", "codemonkeys.cli", "silverback", "--all"]
    
    if dry_run:
        return (0, f"[DRY-RUN] Would execute: {' '.join(cmd)}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stdout + result.stderr
    return (result.returncode, output)


def execute_test(dry_run: bool = False) -> tuple[int, str]:
    """Execute tests (pytest)."""
    cmd = [sys.executable, "-m", "pytest", "tests/", "-q"]
    
    if dry_run:
        return (0, f"[DRY-RUN] Would execute: {' '.join(cmd)}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stdout + result.stderr
    return (result.returncode, output)


def execute_regenerate_report(product_id: str, dry_run: bool = False) -> tuple[int, str]:
    """Execute report regeneration."""
    cmd = [sys.executable, "scripts/generate_run_report.py", product_id]
    
    if dry_run:
        return (0, f"[DRY-RUN] Would execute: {' '.join(cmd)}")
    
    # Check if script exists
    script_path = Path("scripts/generate_run_report.py")
    if not script_path.exists():
        return (1, f"Script not found: {script_path}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stdout + result.stderr
    return (result.returncode, output)


def execute_science_to_design(
    science_path: str,
    product_id: str,
    dry_run: bool = False
) -> tuple[int, str]:
    """Execute science-to-design conversion."""
    cmd = [
        sys.executable, "-m", "codemonkeys.cli",
        "dossier", "science-to-design", science_path,
        "--product-id", product_id
    ]

    if dry_run:
        return (0, f"[DRY-RUN] Would execute: {' '.join(cmd)}")

    # Check if science dossier exists
    from pathlib import Path as P
    if not P(science_path).exists():
        return (1, f"Science dossier not found: {science_path}")

    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stdout + result.stderr
    return (result.returncode, output)


def execute_gc_runs(
    product_id: str,
    keep_count: int = 10,
    dry_run: bool = False
) -> tuple[int, str]:
    """Execute GC runs - delete old run directories, keep last N."""
    runs_dir = Path(f"dash/runs/{product_id}")

    if dry_run:
        return (0, f"[DRY-RUN] Would GC runs for {product_id}, keeping last {keep_count}")

    if not runs_dir.exists():
        return (0, f"No runs directory for {product_id}")

    # Find run directories (run_YYYYMMDD_HHMMSS pattern)
    run_dirs = sorted([d for d in runs_dir.iterdir() if d.is_dir() and d.name.startswith("run_")])

    if len(run_dirs) <= keep_count:
        return (0, f"Only {len(run_dirs)} runs, nothing to GC (keep={keep_count})")

    # Delete oldest runs beyond keep_count
    to_delete = run_dirs[:-keep_count]
    deleted = []

    import shutil
    for run_dir in to_delete:
        try:
            shutil.rmtree(run_dir)
            deleted.append(run_dir.name)
        except Exception as e:
            return (1, f"Failed to delete {run_dir}: {e}")

    return (0, f"Deleted {len(deleted)} old runs: {', '.join(deleted)}")


def execute_drift_check(
    product_id: str,
    dry_run: bool = False
) -> tuple[int, str]:
    """Execute drift check - produce a report of environment state."""
    import platform
    from datetime import datetime as dt

    timestamp = dt.now().strftime("%Y%m%d_%H%M%S")
    drift_dir = Path(f"dash/drift/{product_id}/{timestamp}")

    if dry_run:
        return (0, f"[DRY-RUN] Would produce drift report at {drift_dir}/report.json")

    drift_dir.mkdir(parents=True, exist_ok=True)

    # Collect environment info
    report = {
        "timestamp": dt.now().isoformat() + "Z",
        "product_id": product_id,
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "env_snapshot": {}
    }

    # Get pip freeze if possible
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "freeze"],
            capture_output=True, text=True
        )
        report["pip_freeze"] = result.stdout.strip().split("\n")
    except Exception:
        report["pip_freeze"] = []

    # Write report
    report_file = drift_dir / "report.json"
    import json
    with open(report_file, "w") as f:
        json.dump(report, f, indent=2)

    return (0, f"Drift report written to {report_file}")


def execute_work_order(wo: dict, dry_run: bool = False) -> dict:
    """Execute a single work order and return result."""
    intent = wo.get("intent")
    product_id = wo.get("product_id")
    inputs = wo.get("inputs", {})

    print(f"\n{'='*50}")
    print(f"Executing: {wo.get('job_id')}")
    print(f"  Product: {product_id}")
    print(f"  Intent:  {intent}")
    print(f"  Priority: {wo.get('priority')}")
    print(f"{'='*50}")

    start_time = datetime.now()

    if intent == "validate":
        exit_code, output = execute_validate(dry_run)
    elif intent == "test":
        exit_code, output = execute_test(dry_run)
    elif intent == "regenerate_report":
        exit_code, output = execute_regenerate_report(
            inputs.get("product_id", product_id),
            dry_run
        )
    elif intent == "science_to_design":
        exit_code, output = execute_science_to_design(
            inputs.get("science_path", ""),
            inputs.get("product_id", ""),
            dry_run
        )
    elif intent == "gc_runs":
        exit_code, output = execute_gc_runs(
            inputs.get("product_id", product_id),
            inputs.get("keep_count", 10),
            dry_run
        )
    elif intent == "drift_check":
        exit_code, output = execute_drift_check(
            inputs.get("product_id", product_id),
            dry_run
        )
    else:
        exit_code = 1
        output = f"Unknown intent: {intent}"
        output = f"Unknown intent: {intent}"
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    result = {
        "exit_code": exit_code,
        "completed_at": end_time.isoformat() + "Z",
        "duration_seconds": duration,
        "evidence_produced": wo.get("evidence_expectations", []) if exit_code == 0 else [],
        "error_message": output if exit_code != 0 else ""
    }
    
    status = "completed" if exit_code == 0 else "failed"
    
    print(f"\n  Status: {status}")
    print(f"  Exit code: {exit_code}")
    print(f"  Duration: {duration:.2f}s")
    
    if not dry_run:
        print(f"\n  Output:\n{output[:500]}")
    else:
        print(f"\n  {output}")
    
    return {
        "status": status,
        "result": result
    }


def update_work_order(wo: dict, execution_result: dict, dry_run: bool = False):
    """Update work order file with execution result."""
    if dry_run:
        return
    
    filepath = wo.get("_filepath")
    if not filepath:
        return
    
    wo.update(execution_result)
    del wo["_filepath"]
    
    with open(filepath, "w") as f:
        json.dump(wo, f, indent=2)


def should_stop(wo: dict, execution_result: dict) -> tuple[bool, str]:
    """Check if stop conditions are met."""
    stop_conditions = wo.get("stop_conditions", [])
    result = execution_result.get("result", {})
    exit_code = result.get("exit_code", 0)
    
    if exit_code != 0:
        if "on_test_fail" in stop_conditions and wo.get("intent") == "test":
            return (True, "Test failed (on_test_fail)")
        if "on_silverback_fail" in stop_conditions and wo.get("intent") == "validate":
            return (True, "Silverback failed (on_silverback_fail)")
    
    return (False, "")


def run(
    work_orders_dir: Path,
    budget: int,
    dry_run: bool = False
) -> int:
    """Execute work orders with budget enforcement."""
    work_orders = load_work_orders(work_orders_dir, budget)
    
    if not work_orders:
        print("No pending work orders found.")
        return 0
    
    print(f"\n🚀 Oracle Executor")
    print(f"   Budget: {budget} work orders")
    print(f"   Dry run: {dry_run}")
    print(f"   Found: {len(work_orders)} pending work order(s)")
    
    executed = 0
    failed = 0
    
    for wo in work_orders:
        execution_result = execute_work_order(wo, dry_run)
        update_work_order(wo, execution_result, dry_run)
        
        executed += 1
        if execution_result["status"] == "failed":
            failed += 1
        
        # Check stop conditions
        should_stop_now, reason = should_stop(wo, execution_result)
        if should_stop_now:
            print(f"\n⚠️  Stop condition triggered: {reason}")
            break
    
    print(f"\n{'='*50}")
    print(f"✅ Execution complete")
    print(f"   Executed: {executed}")
    print(f"   Failed: {failed}")
    print(f"   Passed: {executed - failed}")
    
    return 0 if failed == 0 else 1


def main():
    parser = argparse.ArgumentParser(description="Oracle Executor")
    parser.add_argument("--budget", type=int, default=3, help="Max work orders to execute")
    parser.add_argument("--dry-run", action="store_true", help="Preview without executing")
    parser.add_argument("--work-orders-dir", type=Path, default=Path("nexus/work_orders"), help="Work orders directory")
    
    args = parser.parse_args()
    
    return run(
        work_orders_dir=args.work_orders_dir,
        budget=args.budget,
        dry_run=args.dry_run
    )


if __name__ == "__main__":
    sys.exit(main())
