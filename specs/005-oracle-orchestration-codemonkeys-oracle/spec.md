# Spec: Oracle Orchestration

Dossier: DOS-20251222-oracle-orchestration
Constitution: constitution.md
Status: Draft
Owner: nexus
Epic: Oracle Orchestration (Sprint 5)

## 1. Intent
Operators must manually decide what to do next across multiple products; there is no bounded, prioritized work queue.
An Oracle command produces bounded, prioritized next actions with hard stop conditions, enabling fleet-scale operations.

## 2. User Stories
- **As an Operator**, I want to run `codemonkeys oracle plan` to see what actions are needed across my product fleet.
- **As an Operator**, I want to run `codemonkeys oracle run --dry-run` to preview actions before execution.
- **As Nexus**, I want to execute bounded safe jobs (validate, test, report) without violating governance.
- **As an Operator**, I want work orders to include budgets and stop conditions so execution never runs unbounded.

## 3. Functional Requirements
- **FR-001**: Work order schema with fields: `job_id`, `product_id`, `intent`, `inputs`, `budget`, `stop_conditions`, `priority`, `evidence_expectations`.
- **FR-002**: `codemonkeys oracle plan [--budget N]` reads Dash + PM artifacts and emits up to N work orders as JSON.
- **FR-003**: `codemonkeys oracle run [--dry-run]` executes work orders with budget enforcement.
- **FR-004**: Safe job types: `validate`, `test`, `regenerate_report`. No code editing.
- **FR-005**: All executed jobs produce evidence artifacts in `dash/runs/<product_id>/`.

## 4. Acceptance Criteria
- **AC-001**: `codemonkeys oracle plan --budget 3` emits exactly 3 work orders.
- **AC-002**: Work orders conform to `nexus/schemas/work_order.schema.json`.
- **AC-003**: `codemonkeys oracle run --dry-run` shows planned actions without mutation.
- **AC-004**: `codemonkeys oracle run` executes 1 safe job and produces evidence.
- **AC-005**: Execution stops if budget exceeded or stop condition triggered.

## 5. Owner & Authority
- **Feature Owner**: nexus
- **Governance**: Inherits from Dossier DOS-20251222-oracle-orchestration.
- **Approval**: Human Operator.

## 6. Budget & Stop Conditions
- **Budget**: Max 3 work orders per `oracle plan` by default; configurable via `--budget`.
- **Stop Condition**: Kill switch enabled in any product, Silverback failure, test failure.

## 7. Constraints & Non-goals
### Constraints
- **C-001**: Oracle must produce deterministic output given same inputs.
- **C-002**: Execution must respect budget limits (max steps, max time).
- **C-003**: Evidence artifacts are mandatory for all executed jobs.

### Non-goals
- **NG-001**: Code editing or PR generation.
- **NG-002**: LLM-based planning or generation.
- **NG-003**: Multi-agent coordination or parallel execution.

## 8. Evidence Plan
- **Artifacts**: `nexus/work_orders/*.json` - generated work orders
- **Schema**: `nexus/schemas/work_order.schema.json`
- **Tests**: `tests/oracle/test_oracle_plan.py`, `tests/oracle/test_oracle_run.py`
- **Run reports**: Updated `dash/runs/<product_id>/last_run.json`

## 9. Traceability Map
| Requirement | File/Component | Test Case | Status |
|-------------|----------------|-----------|--------|
| FR-001 | `nexus/schemas/work_order.schema.json` | `tests/oracle/test_schema.py` | Pending |
| FR-002 | `src/codemonkeys/commands/oracle.py` | `tests/oracle/test_oracle_plan.py` | Pending |
| FR-003 | `src/codemonkeys/commands/oracle.py` | `tests/oracle/test_oracle_run.py` | Pending |
| FR-004 | `scripts/oracle_executor.py` | `tests/oracle/test_safe_jobs.py` | Pending |
