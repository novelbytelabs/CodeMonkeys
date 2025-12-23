---
schema_version: "0.1"
dossier_id: "DOS-20251222-fleet-ops-schedules-and-science-lane"
product_id: "codemonkeys-fleet-ops"
owner: "nexus"
status: "approved"
created_at: "2025-12-22"
hypothesis:
  problem: "The factory lacks scheduled operations, retention policies, drift detection, and Science Lane visibility in Dash."
  claim: "Adding schedules, GC, drift checks, auto-heal, and Dash Science Lane enables repeatable fleet-wide operations."
  falsification: "If scheduled work orders cannot be generated or executed, or if Dash cannot display Science Lane status."
mvp_boundary:
  in_scope:
    - "Schedule schema and example schedule files"
    - "Oracle planner --from-schedules --product flags"
    - "gc_runs intent with keep N=10 policy"
    - "drift_check intent producing report artifacts"
    - "Auto-heal retry logic (bounded)"
    - "Dash Science Lane panel with index artifact"
  non_goals:
    - "Auto-edit code based on drift"
    - "Complex scheduling (cron expressions)"
    - "Multi-product scheduling dependencies"
acceptance_proofs:
  - "Proof 1: schedule schema validates example schedules"
  - "Proof 2: oracle plan --from-schedules --budget 5 produces bounded work orders"
  - "Proof 3: gc_runs deletes old runs, respects keep=N"
  - "Proof 4: drift_check produces report artifact"
  - "Proof 5: Dash shows Science Lane with status"
evidence:
  links: []
constitution_refs:
  - "constitution.md"
  - "docs/pm/ROADMAP.md"
---

# Design Dossier: Fleet Ops + Dash Science Lane (Sprint 7)

## 1. Context & Problem

The factory can run Oracle work orders, but lacks:
- Scheduled operations (cadence-based planning)
- Retention/GC (old runs pile up)
- Drift detection (environments diverge silently)
- Auto-heal (manual intervention for transient failures)
- Science Lane visibility (no dashboard view)

## 2. Hypothesis

If we add schedules, GC, drift checks, auto-heal, and a Dash Science Lane, then:
- Fleet operations become repeatable and bounded
- Old artifacts are cleaned up safely
- Drift is detected before it causes failures
- Transient failures auto-recover within bounds
- Science handoffs are visible and trackable

## 3. MVP Definition

### In Scope
1. **Schedule Schema**: `dash/schemas/schedule.schema.json`
2. **Schedule Files**: `dash/schedules/<product_id>.json`
3. **Planner Flags**: `--from-schedules`, `--product`
4. **GC Intent**: `gc_runs` (keep N=10, never delete releases)
5. **Drift Intent**: `drift_check` (report only, no auto-edit)
6. **Auto-heal**: retry validate/test once, then stop
7. **Dash Science Lane**: `dash/science_index.json` + UI panel

### Non-goals
- Auto-edit code based on drift reports
- Complex cron-style scheduling
- Multi-product scheduling dependencies
- Real-time Fleet streaming

## 4. Evidence Plan

| Artifact | Purpose |
|----------|---------|
| `dash/schemas/schedule.schema.json` | Schedule format |
| `dash/schedules/codemonkeys-cli.json` | Example schedule |
| `tests/dash/test_schedule_schema.py` | Schema tests |
| `tests/oracle/test_plan_from_schedules.py` | Planner tests |
| `tests/oracle/test_run_gc_runs.py` | GC tests |
| `tests/oracle/test_run_drift_check.py` | Drift tests |
| `tests/oracle/test_auto_heal.py` | Auto-heal tests |
