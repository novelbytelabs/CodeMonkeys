# Autonomy Governance

**Version**: 0.1
**Status**: Active (Bootstrap)
**Applies to**: Nexus Agent, Science Monkeys, Code Monkeys

## Purpose
This document defines **enforceable rules** that govern autonomous operation within Code Monkeys. These rules cannot be bypassed by any agent, including Nexus.

## 1. Core Principles

### 1.1 Nexus Cannot Bypass Gates
The Product Owner (Nexus) is subject to the same verification requirements as any other agent.
- All code changes require passing tests.
- All releases require evidence packs.
- All governance changes require human approval.

### 1.2 Budgets Are Hard Limits
When a budget is exhausted, the operation **must stop**.
- No "borrowing" against future budget.
- No silent continuation.
- Human override required to extend.

### 1.3 Evidence Is Mandatory
No claim is accepted without structured evidence.
- All runs produce `last_run.json` (schema-validated).
- Evidence paths must point to real files.
- "Bootstrap Proof" is acceptable during MVP phase.

---

## 2. Budget Contracts

### 2.1 Per-Run Budgets
| Resource | Default Limit | Override Requires |
|----------|---------------|-------------------|
| Wall time | 15 minutes | Human approval |
| Test runs | 6 | Human approval |
| LLM calls | 4 | Human approval |
| CI retries | 2 | Human approval |
| PRs per wave | 3 | Human approval |

### 2.2 Budget Accounting
- Budgets are tracked in `banana_economy` section of `last_run.json`.
- `spent_minutes` computed from actual timestamps.
- Token tracking: not yet implemented (placeholder 0).

### 2.3 Budget Exhaustion
When any budget is exhausted:
1. Current operation completes its atomic step.
2. No new operations are started.
3. Run report is written with `status: "budget_exhausted"`.
4. Human is notified.

---

## 3. Stop Conditions

Autonomous loops **must stop** when any of these conditions are met:

| Condition | Detection | Action |
|-----------|-----------|--------|
| Budget exhausted | `spent_X >= budget_X` | Stop, write report |
| Repeated CI failure | 3+ consecutive failures | Stop, escalate |
| Scope creep | Diff > 500 lines | Stop, request review |
| Confidence low | Uncertainty flag set | Stop, escalate |
| Missing acceptance hooks | Required proofs undefined | Block implementation |
| Kill switch enabled | `kill_switch.enabled == true` | Immediate stop |

### 3.1 Graceful Stop
When stopping:
1. Complete current atomic operation if possible.
2. Write partial evidence to log file.
3. Write `last_run.json` with failure status.
4. Do not start new operations.

---

## 4. Evidence Requirements

### 4.1 Mandatory Artifacts
Every run **must** produce:
- `last_run.json` (schema-valid)
- `pytest_output.log` (or equivalent test output)

### 4.2 Bootstrap Proof
During MVP/bootstrap phase:
- Screenshots are acceptable evidence.
- Fixtures are acceptable (labeled as fixtures).
- All evidence must be structured (JSON, not prose).

### 4.3 Production Proof
When exiting bootstrap:
- Real test execution results.
- Real CI artifacts.
- No fixture substitution without explicit labeling.

---

## 5. Kill Switch Contract

### 5.1 Definition
A kill switch is a mechanism that **immediately halts** all autonomous operations.

### 5.2 Implementation
- **File-based**: Presence of `.codemonkeys/KILL_SWITCH` file.
- **JSON field**: `kill_switch.enabled == true` in `last_run.json`.
- **Environment**: `CODEMONKEYS_KILL=1` environment variable.

### 5.3 Behavior When Enabled
1. All running agents halt at next checkpoint.
2. No new operations are started.
3. Run reports are written with `kill_switch.enabled: true`.
4. Human intervention required to resume.

### 5.4 Scope
| Scope | Trigger | Effect |
|-------|---------|--------|
| Global | `.codemonkeys/KILL_SWITCH` | All products stop |
| Product | `dash/runs/<product>/KILL_SWITCH` | Single product stops |

---

## 6. Enforcement

### 6.1 Bootstrap (Current)
- Silverback validator script checks compliance.
- `preflight.sh` runs before commits.
- Human reviews evidence packs.

### 6.2 CI Enforcement (Active)
- `.github/workflows/codemonkeys-ci.yml` runs on all PRs to main.
- **Checks enforced**:
  - pytest (schema validation tests)
  - Silverback validation (spec readiness + artifact validity)
  - Run report generation (`last_run.json` must exist)
- **Artifacts uploaded**: pytest log, Silverback log, last_run.json
- **Failure = blocked merge** (when branch protection enabled).

### 6.3 Production (Future)
- CI gates prevent non-compliant merges.
- Nexus cannot approve its own changes.
- Automated evidence collection and validation.

---

## 7. Amendments
This document can only be amended by:
1. Human operator explicit approval.
2. Documented rationale for the change.
3. Updated version number.

No agent may self-modify governance rules.

---

## 8. Branching Workflow

### Branch Roles
| Branch | Purpose | Direct Commits |
|--------|---------|----------------|
| `main` | Stable/release | ❌ PRs only |
| `dev` | Integration | ❌ PRs only |
| `feature/*` | Work branches | ✅ |

### PR Flow
1. Create `feature/<name>` from `dev`
2. Work on feature, commit freely
3. PR `feature/*` → `dev` (CI must pass)
4. PR `dev` → `main` when ready for release (CI + review)

### Starting New Work
```bash
git checkout dev
git pull origin dev
git checkout -b feature/<short-name>
git push -u origin feature/<short-name>
```

### CI Triggers
- Push to `dev`: runs CI
- PR to `dev`: runs CI
- PR to `main`: runs CI

### Branch Protection (Recommended)
- `main`: Require PRs, require status checks, no direct pushes
- `dev`: Require status checks
