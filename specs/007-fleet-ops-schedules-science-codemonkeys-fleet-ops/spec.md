# Spec: Fleet Ops + Dash Science Lane (Sprint 7)

Dossier: DOS-20251222-fleet-ops-schedules-and-science-lane
Constitution: constitution.md
Status: Draft
Owner: nexus
Epic: Fleet Ops

## 1. Intent
The factory lacks scheduled operations, retention policies, drift detection, and Science Lane visibility in Dash.
Adding schedules, GC, drift checks, auto-heal, and Dash Science Lane enables repeatable fleet-wide operations.

## 2. User Stories
- **As an Operator**, I want to define schedules for each product so jobs run automatically at defined cadences.
- **As Nexus**, I want work orders generated from schedules so planning is deterministic and bounded.
- **As Nexus**, I want old run directories cleaned up automatically so storage doesn't grow unbounded.
- **As an Operator**, I want drift reports so I can detect environment divergence before failures.
- **As an Operator**, I want to see Science Lane status in Dash so I can track handoff progress.

## 3. Functional Requirements
- **FR-001**: Schedule schema in `dash/schemas/schedule.schema.json` with cadence, jobs, enabled fields.
- **FR-002**: `codemonkeys oracle plan --from-schedules` generates work orders from schedule files.
- **FR-003**: `codemonkeys oracle plan --product <id>` filters to single product.
- **FR-004**: `gc_runs` intent deletes old run directories, keeping last N (default 10).
- **FR-005**: `drift_check` intent produces `dash/drift/<product>/<timestamp>/report.json`.
- **FR-006**: Dash Science Lane panel shows science dossiers with status.

## 4. Acceptance Criteria
- **AC-001**: Schedule schema validates example schedules.
- **AC-002**: `oracle plan --from-schedules --budget 5` produces bounded work orders.
- **AC-003**: `gc_runs` deletes old runs, respects keep=N.
- **AC-004**: `drift_check` produces report artifact.
- **AC-005**: Dash shows Science Lane with status.

## 5. Owner & Authority
- **Feature Owner**: nexus
- **Governance**: Inherits from Dossier DOS-20251222-fleet-ops-schedules-and-science-lane.
- **Approval**: Human Operator.

## 6. Budget & Stop Conditions
- **Budget**: Max 5 work orders per scheduled run.
- **Stop Condition**: Kill switch, on_test_fail, on_silverback_fail.

## 7. Constraints & Non-goals
### Constraints
- **C-001**: GC never deletes release records.
- **C-002**: Drift check is report-only (no auto-edit).
- **C-003**: Auto-heal limited to retry once.

### Non-goals
- **NG-001**: Auto-edit code based on drift.
- **NG-002**: Complex scheduling (cron expressions).
- **NG-003**: Multi-product scheduling dependencies.

## 8. Evidence Plan
- **Artifacts**: `dash/schemas/schedule.schema.json`, schedule example, drift reports.
- **Tests**: `tests/dash/test_schedule_schema.py`, `tests/oracle/test_plan_from_schedules.py`.

## 9. Traceability Map
| Source | Target | Relation |
|--------|--------|----------|
| `DOS-20251222-fleet-ops-schedules-and-science-lane.md` | `specs/007-.../spec.md` | dossier → spec |
| `schedule.schema.json` | Work order generation | schema → planner |
