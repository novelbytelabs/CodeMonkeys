#!/usr/bin/env python3
"""
Generate Run Report for Code Monkeys Dash.

Runs pytest, captures output, and writes a structured last_run.json artifact.

Usage:
    python scripts/generate_run_report.py <product_id> [--test-path <path>]

Example:
    python scripts/generate_run_report.py codemonkeys-dash --test-path tests/dash/
"""
import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def get_timestamp():
    """Return current timestamp in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat()


def generate_run_id():
    """Generate a unique run ID based on timestamp."""
    now = datetime.now(timezone.utc)
    return f"run_{now.strftime('%Y%m%d_%H%M%S')}"


def run_pytest(test_path: str, output_file: Path) -> tuple[int, str]:
    """
    Run pytest and capture output.

    Returns:
        tuple: (exit_code, summary)
    """
    cmd = [
        "conda", "run", "-n", "helios-gpu-118",
        "pytest", test_path, "-v", "--tb=short"
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        # Write full output to log file
        output_file.write_text(result.stdout + result.stderr)
        
        # Parse summary
        if result.returncode == 0:
            summary = "All tests passed"
        else:
            # Try to extract failure summary
            lines = result.stdout.split('\n')
            summary_line = [l for l in lines if 'failed' in l.lower() or 'error' in l.lower()]
            summary = summary_line[0] if summary_line else "Tests failed"
        
        return result.returncode, summary
        
    except subprocess.TimeoutExpired:
        return 2, "Test run timed out"
    except Exception as e:
        return 2, f"Error running tests: {e}"


def generate_report(
    product_id: str,
    run_id: str,
    start_time: str,
    end_time: str,
    exit_code: int,
    summary: str,
    evidence_paths: list[str]
) -> dict:
    """Generate a run report dictionary."""
    return {
        "schema_version": "0.1",
        "product_id": product_id,
        "run_id": run_id,
        "started_at": start_time,
        "ended_at": end_time,
        "status": "success" if exit_code == 0 else "failed",
        "summary": summary,
        "evidence": {
            "paths": evidence_paths
        },
        "banana_economy": {
            "budget_tokens": 50000,
            "spent_tokens": 0,  # Not tracked yet
            "budget_minutes": 90,
            "spent_minutes": 0,  # Calculate from start/end
            "max_ci_heal_attempts": 2,
            "ci_heal_attempts_used": 0
        },
        "kill_switch": {
            "enabled": False,
            "reason": ""
        },
        "pr_wave": {
            "state": "none",
            "open_prs": 0,
            "last_update": end_time
        }
    }


def main():
    parser = argparse.ArgumentParser(description="Generate run report for Dash")
    parser.add_argument("product_id", help="Product identifier (e.g., codemonkeys-dash)")
    parser.add_argument("--test-path", default="tests/", help="Path to tests")
    parser.add_argument("--output-dir", default="dash/runs", help="Output directory")
    args = parser.parse_args()

    # Setup paths
    run_id = generate_run_id()
    output_dir = Path(args.output_dir) / args.product_id
    run_dir = output_dir / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    log_path = run_dir / "pytest_output.log"
    report_path = output_dir / "last_run.json"

    print(f"[*] Starting run: {run_id}")
    print(f"[*] Product: {args.product_id}")
    print(f"[*] Test path: {args.test_path}")

    # Run tests
    start_time = get_timestamp()
    exit_code, summary = run_pytest(args.test_path, log_path)
    end_time = get_timestamp()

    print(f"[*] Exit code: {exit_code}")
    print(f"[*] Summary: {summary}")

    # Build evidence paths
    evidence_paths = [
        f"runs/{args.product_id}/{run_id}/pytest_output.log",
    ]

    # Generate report
    report = generate_report(
        product_id=args.product_id,
        run_id=run_id,
        start_time=start_time,
        end_time=end_time,
        exit_code=exit_code,
        summary=summary,
        evidence_paths=evidence_paths
    )

    # Write report
    report_path.write_text(json.dumps(report, indent=2))
    print(f"[*] Report written to: {report_path}")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
