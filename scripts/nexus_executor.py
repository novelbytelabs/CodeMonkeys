#!/usr/bin/env python3
"""
Nexus Executor

Applies decisions from Nexus outbox to target artifacts.

Supported decision types:
- budget_grant: Updates banana_economy.budget_tokens in run artifacts
- kill_switch_toggle: Enables/disables kill_switch in run artifacts
- approval: Marks request as acknowledged
- rejection: Marks request as acknowledged

Usage:
    python scripts/nexus_executor.py                    # Process all pending decisions
    python scripts/nexus_executor.py --decision DEC_ID  # Process specific decision
    python scripts/nexus_executor.py --dry-run          # Show what would be done
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

NEXUS_OUTBOX = Path("nexus/outbox")
NEXUS_INBOX = Path("nexus/inbox")
DASH_RUNS = Path("dash/runs")


def get_timestamp():
    """Return current timestamp in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat()


def atomic_write_json(path: Path, data: dict):
    """Write JSON atomically."""
    tmp_path = path.with_suffix(".json.tmp")
    tmp_path.write_text(json.dumps(data, indent=2))
    os.replace(tmp_path, path)


def load_decision(decision_path: Path) -> dict | None:
    """Load a decision from the outbox."""
    try:
        return json.loads(decision_path.read_text())
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"[ERROR] Failed to load decision {decision_path}: {e}")
        return None


def load_run_artifact(product_id: str) -> tuple[Path, dict] | tuple[None, None]:
    """Load the last_run.json for a product."""
    run_path = DASH_RUNS / product_id / "last_run.json"
    if not run_path.exists():
        return None, None
    try:
        return run_path, json.loads(run_path.read_text())
    except json.JSONDecodeError as e:
        print(f"[ERROR] Failed to load run artifact for {product_id}: {e}")
        return None, None


def apply_budget_grant(decision: dict, dry_run: bool = False) -> bool:
    """Apply a budget_grant decision to the target product."""
    target = decision.get("target")
    payload = decision.get("payload", {})
    granted = payload.get("granted_tokens", 0)
    new_total = payload.get("new_total_budget")
    
    if not target:
        print(f"[ERROR] Decision {decision['decision_id']}: missing target")
        return False
    
    run_path, artifact = load_run_artifact(target)
    if artifact is None:
        print(f"[WARN] No run artifact for {target}, cannot apply budget grant")
        return False
    
    old_budget = artifact.get("banana_economy", {}).get("budget_tokens", 0)
    
    if new_total is not None:
        new_budget = new_total
    else:
        new_budget = old_budget + granted
    
    if dry_run:
        print(f"[DRY-RUN] Would update {target}: budget_tokens {old_budget} → {new_budget}")
        return True
    
    artifact["banana_economy"]["budget_tokens"] = new_budget
    atomic_write_json(run_path, artifact)
    print(f"[OK] Applied budget grant to {target}: {old_budget} → {new_budget}")
    return True


def apply_kill_switch(decision: dict, dry_run: bool = False) -> bool:
    """Apply a kill_switch_toggle decision to the target product."""
    target = decision.get("target")
    payload = decision.get("payload", {})
    enable = payload.get("enabled", False)
    reason = payload.get("reason", "Nexus directive")
    
    if not target:
        print(f"[ERROR] Decision {decision['decision_id']}: missing target")
        return False
    
    run_path, artifact = load_run_artifact(target)
    if artifact is None:
        print(f"[WARN] No run artifact for {target}, cannot apply kill switch")
        return False
    
    old_state = artifact.get("kill_switch", {}).get("enabled", False)
    
    if dry_run:
        print(f"[DRY-RUN] Would update {target}: kill_switch {old_state} → {enable}")
        return True
    
    artifact["kill_switch"]["enabled"] = enable
    artifact["kill_switch"]["reason"] = reason
    atomic_write_json(run_path, artifact)
    print(f"[OK] Set kill_switch for {target}: {old_state} → {enable}")
    return True


def mark_decision_executed(decision_path: Path, decision: dict):
    """Update decision status to 'executed'."""
    decision["status"] = "executed"
    decision["executed_at"] = get_timestamp()
    atomic_write_json(decision_path, decision)


def process_decision(decision_path: Path, dry_run: bool = False) -> bool:
    """Process a single decision."""
    decision = load_decision(decision_path)
    if decision is None:
        return False
    
    decision_id = decision.get("decision_id", "unknown")
    decision_type = decision.get("type")
    status = decision.get("status")
    
    # Skip already executed decisions
    if status == "executed":
        print(f"[SKIP] {decision_id}: already executed")
        return True
    
    # Only process 'issued' decisions
    if status != "issued":
        print(f"[SKIP] {decision_id}: status is '{status}', not 'issued'")
        return True
    
    print(f"[*] Processing {decision_id} (type: {decision_type})")
    
    success = False
    if decision_type == "budget_grant":
        success = apply_budget_grant(decision, dry_run)
    elif decision_type == "kill_switch_toggle":
        success = apply_kill_switch(decision, dry_run)
    elif decision_type in ("approval", "rejection", "directive", "allocation"):
        # These don't modify artifacts directly, just mark as executed
        print(f"[OK] Acknowledged {decision_type} decision")
        success = True
    else:
        print(f"[WARN] Unknown decision type: {decision_type}")
        return False
    
    if success and not dry_run:
        mark_decision_executed(decision_path, decision)
        print(f"[OK] Marked {decision_id} as executed")
    
    return success


def process_all_decisions(dry_run: bool = False) -> tuple[int, int]:
    """Process all pending decisions in the outbox."""
    if not NEXUS_OUTBOX.exists():
        print("[WARN] Nexus outbox directory not found")
        return 0, 0
    
    decisions = list(NEXUS_OUTBOX.glob("*.json"))
    if not decisions:
        print("[INFO] No decisions in outbox")
        return 0, 0
    
    success_count = 0
    fail_count = 0
    
    for decision_path in decisions:
        if process_decision(decision_path, dry_run):
            success_count += 1
        else:
            fail_count += 1
    
    return success_count, fail_count


def main():
    parser = argparse.ArgumentParser(description="Nexus Decision Executor")
    parser.add_argument("--decision", help="Process specific decision by ID")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done")
    args = parser.parse_args()
    
    print("\n=== Nexus Executor ===\n")
    
    if args.decision:
        decision_path = NEXUS_OUTBOX / f"{args.decision}.json"
        if not decision_path.exists():
            print(f"[ERROR] Decision not found: {decision_path}")
            return 1
        success = process_decision(decision_path, args.dry_run)
        return 0 if success else 1
    else:
        success, fail = process_all_decisions(args.dry_run)
        print(f"\n=== Summary ===")
        print(f"Processed: {success}")
        print(f"Failed: {fail}")
        return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
