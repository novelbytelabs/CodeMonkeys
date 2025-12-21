# CodeMonkeys v0.1: Refined Architecture (Post-Critique)

> **Critiques Applied:** Gemini, Grok, GPT-5.2 (2025-12-20)

---

## Executive Summary: Key Fixes Applied

| Issue | Original | Fixed |
|-------|----------|-------|
| **Too many agents** | 6 agents in v0.1 | **3 agents**: Silverback + Code Monkey + Foreman |
| **Static Banana pricing** | Fixed costs | **Time-based**: 1 sec wall-clock = 1 🍌 |
| **Foreman gap** | Plan → Build | Plan → **Silverback validates** → Build |
| **Scout scope creep** | Full agent | **Deferred to v0.2**, read-only when added |
| **Chaos fuzz vs fault** | Mixed | **Split**: `chaos fuzz` vs `chaos fault` |
| **governance.lock** | Undefined | **Hash-based lockfile** with tool versions |
| **Observer role** | Full agent | **Cross-cutting concern** (RunReport ledger) |
| **Multi-resource budgets** | Single scalar | **Multi-wallet**: time / runs / LLM calls |

---

## 1. The Troop v0.1 (Minimum Viable Factory)

| Agent | Role | Command | Status |
|-------|------|---------|--------|
| 🦍 **Silverback** | Governance | `codemonkeys check` | **v0.1** |
| 🐒 **Code Monkey** | Builder | `codemonkeys heal` | **v0.1** |
| 🦧 **Foreman** | Planner | `codemonkeys plan` | **v0.1** |
| 🐵 **Chaos Monkey** | Fuzzer | `codemonkeys chaos` | **v0.2** |
| 🐵 **Scout** | Reconnaissance | `codemonkeys scout` | **v0.2** |

### Capabilities Matrix (GPT Fix)

| Agent | Write Code | Run Tests | Modify Config | Propose Rules | Enforce Blocks |
|-------|------------|-----------|---------------|---------------|----------------|
| **Silverback** | ❌ | ✅ | ❌ | ✅ | ✅ |
| **Code Monkey** | ✅ | ✅ | ✅ (scoped) | ✅ | ❌ |
| **Foreman** | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Chaos** (v0.2) | ❌ | ✅ (fuzz) | ❌ | ✅ (findings) | ❌ |
| **Scout** (v0.2) | ❌ | ✅ (read) | ❌ | ✅ (drafts) | ❌ |

---

## 2. The Constitution (Refined)

### 2.1 Rule Block Format (Enhanced)

```markdown
## Rule: No Secrets
Severity: error

\`\`\`codemonkeys-rule
id: "gov.no_secrets"
version: "1"
since: "2025-12-20"
severity: "error"
check:
  kind: "secret_scan"
  patterns:
    - "AKIA[0-9A-Z]{16}"
message: "Secret detected. Remove and rotate."
\`\`\`
```

### 2.2 governance.lock (GPT Fix)

**Deterministic lockfile with hashes:**

```yaml
lock_version: 1
constitution_hash: "sha256:abc123..."
generated_at: "2025-12-20T14:31:00Z"
codemonkeys_version: "0.1.0"
tools:
  gitleaks: "8.21.0"
  clippy: "0.1.83"
rules:
  - id: "gov.no_secrets"
    version: "1"
    severity: "error"
    patterns_hash: "sha256:def456..."
```

### 2.3 Exit Codes (GPT Fix)

| Exit Code | Meaning |
|-----------|---------|
| `0` | No errors (warnings may exist) |
| `1` | Errors present |
| `2` | Internal failure (tool crash) |
| `3` | Warnings present (only with `--strict`) |

### 2.4 CLI Flags

```bash
codemonkeys check                    # Normal mode
codemonkeys check --compile          # Generate governance.lock
codemonkeys check --strict           # Warnings → Errors
codemonkeys check --format sarif     # CI-friendly output
codemonkeys check --changed-only     # PR performance
```

---

## 3. Banana Economy v2 (Multi-Wallet)

### 3.1 Multi-Resource Budgets (GPT Fix)

```yaml
economy:
  budgets:
    wall_time_seconds: 900    # 15 minutes
    test_runs: 6
    llm_calls: 4
    build_runs: 3
  costs:
    cargo_test:
      test_runs: 1
      wall_time_seconds: 120  # Estimated
    llm_call:
      llm_calls: 1
      wall_time_seconds: 60
    cargo_build:
      build_runs: 1
      wall_time_seconds: 180
```

### 3.2 Dynamic Pricing (Gemini Fix)

Instead of static costs, measure **actual wall-clock time**:

```rust
// Pseudo-code
let start = Instant::now();
cargo_test()?;
let elapsed = start.elapsed();
ledger.charge_time(elapsed);
```

### 3.3 Ledger Persistence (GPT Fix)

Store at `.codemonkeys/runs/<run_id>/ledger.json`:

```json
{
  "run_id": "2025-12-20-001",
  "actions": [
    {"action": "cargo_test", "cost_seconds": 45, "result": "pass"},
    {"action": "llm_call", "cost_seconds": 12, "result": "fix_proposed"}
  ],
  "remaining": {"wall_time_seconds": 843, "test_runs": 5}
}
```

---

## 4. Chaos Monkey v0.2 (Split Design)

### 4.1 Separate Modes (GPT Fix)

```bash
codemonkeys chaos fuzz --lane function --time 2m   # Fuzzing
codemonkeys chaos fault --scenario disk_full       # Fault injection
```

### 4.2 Fuzzing Engine (Gemini Fix)

**Default to `proptest`** (stable Rust), not `cargo-fuzz` (nightly):

| Mode | Tool | Rust Channel |
|------|------|--------------|
| Default | `proptest` | Stable |
| Advanced | `cargo-fuzz` | Nightly (opt-in) |

### 4.3 Network Allowlist (Gemini Fix)

```yaml
chaos:
  allow_hosts:
    - "localhost"
    - "127.0.0.1"
    - "postgres-local"  # Docker container
  deny_hosts:
    - "*"
```

### 4.4 HTTP Oracles (GPT Fix)

```yaml
chaos:
  http:
    oracles:
      - kind: "status_allowlist"
        allowed: [200, 400, 401, 403, 404, 422]
      - kind: "max_latency_ms"
        p99: 500
      - kind: "json_schema"
        schema_path: "openapi.json"
```

---

## 5. Shared Artifact Format: RunReport (GPT Fix)

All agents output to `.codemonkeys/runs/<run_id>/report.json`:

```json
{
  "run_id": "2025-12-20-001",
  "agent": "silverback",
  "command": "check",
  "started_at": "2025-12-20T14:30:00Z",
  "finished_at": "2025-12-20T14:30:12Z",
  "exit_code": 1,
  "inputs": {
    "config_hash": "sha256:...",
    "constitution_hash": "sha256:..."
  },
  "findings": [
    {"rule_id": "gov.no_secrets", "file": "config.env", "line": 42}
  ],
  "artifacts": ["governance.lock", "sarif.json"],
  "next_action": "codemonkeys heal --from-check 2025-12-20-001"
}
```

---

## 6. Workflow Refinement (Gemini Fix)

### Plan Validation Loop

**Before:** `Foreman → Code Monkey → Silverback (post-check)`
**After:** `Foreman → Silverback (pre-check) → Code Monkey → Silverback (post-check)`

```
1. User: codemonkeys plan "Add OAuth"
2. Foreman: Generates plan.yaml
3. Silverback: Validates plan (e.g., "Plan adds unsafe block → needs approval")
4. Code Monkey: Builds ticket T1
5. Silverback: Checks final code
6. Observer ledger: Records outcome
```

---

## 7. Scout Boundaries (GPT Fix) — v0.2

When implemented, Scout will be strictly bounded:

1. **Never writes code** — read-only
2. **Never opens PRs** — suggestions only
3. **Default offline** — no LLM unless `--remote` flag
4. **Output format** — structured YAML, not prose

```yaml
scout_report:
  repo_facts:
    languages: ["rust"]
  risks:
    - id: "risk.missing_tests"
      confidence: 0.72
  suggested_rules:
    - draft_id: "rust.no_db_in_handlers"
      rationale: "handlers import sqlx directly"
```

---

## 8. Revised Roadmap

| Priority | Task | Agent |
|----------|------|-------|
| **P0** | Constitution parser + `governance.lock` | Silverback |
| **P0** | `codemonkeys check` with SARIF output | Silverback |
| **P0** | Banana Economy ledger (multi-wallet) | Core |
| **P1** | `codemonkeys heal` with max 3 iterations | Code Monkey |
| **P1** | `codemonkeys plan` → plan.yaml | Foreman |
| **P1** | Plan validation by Silverback | Silverback |
| **P2** | `codemonkeys chaos fuzz --lane function` | Chaos |
| **P2** | `codemonkeys scout` (read-only) | Scout |
| **P3** | `codemonkeys chaos fault` | Chaos |

---

## 9. Risk Tracker

| Risk | Mitigation |
|------|------------|
| Scout scope creep | Strict capabilities matrix, defer to v0.2 |
| Governance too strict | `RUST-01` (no unwrap) is Warning, not Error |
| External tool deps | Auto-detect, provide "capability missing" messages |
| Nondeterministic Chaos | Stable seeds + ledger + artifacts |
| Sandbox promises | Tier-based: bwrap (Linux) > tempdir (fallback) |
| PR can't merge (CLI) | Provide GitHub Action workflow, SARIF output |
