---
schema_version: "0.1"
dossier_id: "DOS-20251222-oracle-orchestration"
product_id: "codemonkeys-oracle"
owner: "nexus"
status: "approved"
created_at: "2025-12-22"
hypothesis:
  problem: "Operators must manually decide what to do next across multiple products; there is no bounded, prioritized work queue."
  claim: "An Oracle command produces bounded, prioritized next actions with hard stop conditions, enabling fleet-scale operations."
  falsification: "If Oracle cannot produce deterministic work orders given fixed inputs, or if execution violates budgets/stop conditions."
mvp_boundary:
  in_scope:
    - "Work order schema with budget and stop conditions"
    - "codemonkeys oracle plan command that emits bounded work orders"
    - "codemonkeys oracle run --dry-run to preview execution"
    - "Safe job types: validate, test, regenerate run report"
  non_goals:
    - "Code editing or PR generation"
    - "LLM-based planning"
    - "Multi-agent coordination"
acceptance_proofs:
  - "Proof 1: codemonkeys oracle plan --budget 3 emits exactly 3 work orders"
  - "Proof 2: Work orders conform to nexus/schemas/work_order.schema.json"
  - "Proof 3: codemonkeys oracle run --dry-run shows planned actions without mutation"
  - "Proof 4: codemonkeys oracle run executes 1 safe job and produces evidence"
evidence:
  links: []
constitution_refs:
  - "constitution.md"
  - "docs/pm/00_VISION_STRATEGY.md"
  - "docs/pm/ROADMAP.md"
---

# Design Dossier: Oracle Orchestration (Sprint 5)

## 1. Context & Problem

The factory foundation is complete (v0.4.1):
- Artifacts exist and are validated
- Authority chain is enforced
- Release gate is mechanical
- Silverback is trustworthy (0 errors, 0 warnings)

**Bottleneck now:** Operators must manually decide what to run across products. There is no automated "what should happen next" generator.

## 2. Hypothesis

If we build an Oracle that reads fleet status and produces bounded work orders with hard stop conditions, then:
- Operators get a clear prioritized queue
- Execution is bounded and auditable
- The system moves toward full autonomy without losing governance

**We know we're wrong if:**
- Oracle produces non-deterministic output given same inputs
- Execution violates budgets or ignores stop conditions
- Evidence artifacts are not produced for executed jobs

## 3. MVP Definition

### In Scope
- **Work Order Schema**: `job_id`, `product_id`, `intent`, `inputs`, `budget`, `stop_conditions`, `priority`, `evidence_expectations`
- **`codemonkeys oracle plan`**: Reads Dash + PM docs, emits work orders
- **`codemonkeys oracle run`**: Executes safe jobs with budget enforcement
- **Safe job types only**: validate, test, run report generation (no code edits)

### Out of Scope
- Code generation / editing
- PR creation
- LLM integration
- Multi-product parallel execution

## 4. Evidence Plan

| Artifact | Description |
|----------|-------------|
| `nexus/work_orders/*.json` | Generated work orders |
| `nexus/schemas/work_order.schema.json` | Schema for validation |
| `tests/oracle/test_oracle_plan.py` | Deterministic planning tests |
| `tests/oracle/test_oracle_run.py` | Budget enforcement tests |
| `dash/runs/*/last_run.json` | Updated by executed jobs |
