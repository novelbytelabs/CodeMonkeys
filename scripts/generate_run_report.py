#!/usr/bin/env python3
"""
Generate Run Report for Code Monkeys Dash.

Runs pytest, captures output, and writes a structured last_run.json artifact.

Features:
- Atomic file writes (prevents partial/corrupted artifacts)
- Computes actual spent_minutes from timestamps
- Ensures log file exists even on timeout/exception
- Validates report against schema before exiting success
- CI mode (--ci) runs without conda dependency

Usage:
    # Local (with conda)
    python scripts/generate_run_report.py <product_id> [--test-path <path>]

    # CI (without conda)
    python scripts/generate_run_report.py <product_id> --ci --test-path tests/dash/
"""
import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from jsonschema import validate, ValidationError
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False

SCHEMA_PATH = Path("dash/schemas/last_run.schema.json")


def get_timestamp():
    """Return current timestamp in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat()


def parse_timestamp(ts: str) -> datetime:
    """Parse ISO 8601 timestamp."""
    return datetime.fromisoformat(ts)


def compute_spent_minutes(start: str, end: str) -> float:
    """Compute minutes elapsed between start and end timestamps."""
    start_dt = parse_timestamp(start)
    end_dt = parse_timestamp(end)
    delta = (end_dt - start_dt).total_seconds()
    return round(delta / 60.0, 2)


def generate_run_id():
    """Generate a unique run ID based on timestamp."""
    now = datetime.now(timezone.utc)
    return f"run_{now.strftime('%Y%m%d_%H%M%S')}"


def atomic_write_json(path: Path, data: dict):
    """
    Write JSON atomically using a temp file + os.replace.
    Prevents partial/corrupted artifacts if interrupted mid-write.
    """
    tmp_path = path.with_suffix(".json.tmp")
    tmp_path.write_text(json.dumps(data, indent=2))
    os.replace(tmp_path, path)


def ensure_log_file(log_path: Path, content: str):
    """Ensure log file exists with at least some content."""
    if not log_path.parent.exists():
        log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(content or "[No output captured]")


def run_pytest(test_path: str, output_file: Path, ci_mode: bool = False) -> tuple[int, str]:
    """
    Run pytest and capture output.

    Args:
        test_path: Path to tests
        output_file: Path to write pytest output
        ci_mode: If True, run pytest directly (no conda)

    Returns:
        tuple: (exit_code, summary)
    """
    if ci_mode:
        # CI mode: run pytest directly
        cmd = ["pytest", test_path, "-v", "--tb=short"]
    else:
        # Local mode: use conda environment
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
        full_output = result.stdout + "\n" + result.stderr
        ensure_log_file(output_file, full_output)

        # Parse summary
        if result.returncode == 0:
            summary = "All tests passed"
        else:
            # Try to extract failure summary
            lines = result.stdout.split('\n')
            summary_lines = [l for l in lines if 'failed' in l.lower() or 'error' in l.lower()]
            summary = summary_lines[0] if summary_lines else "Tests failed"

        return result.returncode, summary

    except subprocess.TimeoutExpired as e:
        # Ensure log file exists even on timeout
        stdout = e.stdout.decode() if e.stdout else ''
        stderr = e.stderr.decode() if e.stderr else ''
        partial_output = f"[TIMEOUT after 300s]\nPartial stdout:\n{stdout}\nPartial stderr:\n{stderr}"
        ensure_log_file(output_file, partial_output)
        return 2, "Test run timed out (300s)"

    except Exception as e:
        # Ensure log file exists on any exception
        error_content = f"[EXCEPTION]\n{type(e).__name__}: {e}"
        ensure_log_file(output_file, error_content)
        return 2, f"Error running tests: {e}"


def validate_report(report: dict) -> tuple[bool, str]:
    """
    Validate report against JSON schema.

    Returns:
        tuple: (is_valid, error_message)
    """
    if not HAS_JSONSCHEMA:
        return True, "jsonschema not installed, skipping validation"

    if not SCHEMA_PATH.exists():
        return True, f"Schema not found at {SCHEMA_PATH}, skipping validation"

    try:
        schema = json.loads(SCHEMA_PATH.read_text())
        validate(instance=report, schema=schema)
        return True, "Schema validation passed"
    except ValidationError as e:
        return False, f"Schema validation failed: {e.message}"


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
    spent_minutes = compute_spent_minutes(start_time, end_time)

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
            "spent_tokens": 0,  # Token tracking not implemented yet
            "budget_minutes": 90,
            "spent_minutes": spent_minutes,
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
    parser.add_argument("--ci", action="store_true", help="CI mode: run pytest directly (no conda)")
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
    print(f"[*] CI mode: {args.ci}")

    # Run tests
    start_time = get_timestamp()
    exit_code, summary = run_pytest(args.test_path, log_path, ci_mode=args.ci)
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

    # Validate report against schema
    is_valid, validation_msg = validate_report(report)
    print(f"[*] {validation_msg}")

    if not is_valid:
        print("[!] ERROR: Generated report is invalid. Exiting with error.")
        return 1

    # Write report atomically
    atomic_write_json(report_path, report)
    print(f"[*] Report written atomically to: {report_path}")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
