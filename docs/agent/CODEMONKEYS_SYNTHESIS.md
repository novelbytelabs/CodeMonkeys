# CodeMonkeys Architecture: 6-AI Synthesis

> **Contributors:** Gemini ×2, Grok ×2, GPT-5.2 ×2 (2025-12-20)

---

## 🎯 Unanimous Consensus

| Topic | Agreement |
|-------|-----------|
| **The Troop** | Silverback + Code Monkey + Chaos Monkey + Observer + **Foreman** (new) |
| **Constitution** | Parse `constitution.md` → generate machine rules (YAML) |
| **Chaos Monkey** | Use `cargo-fuzz`/`proptest` for Rust; sandbox-first |
| **Banana Economy** | YES - Token-based budgets to prevent infinite loops |
| **New Agent** | Add a **Planner/Foreman** for ticket breakdown |

---

## 1. The Troop (Finalized)

| Agent | Role | Command | Identity |
|-------|------|---------|----------|
| 🦍 **Silverback** | Governance | `codemonkeys check` | The Gatekeeper |
| 🐒 **Code Monkey** | Builder | `codemonkeys heal` | The Fixer |
| 🐵 **Chaos Monkey** | Fuzzer | `codemonkeys chaos` | The Adversary |
| 🙈 **Observer** | Memory | `codemonkeys status` | The Historian |
| 🦧 **Foreman** | Planner | `codemonkeys plan` | The Architect (NEW) |
| 🐵 **Scout** | Reconnaissance | `codemonkeys scout` | The Explorer (NEW, Grok) |

---

## 2. The Constitution (Silverback Design)

### 2.1 Parsing Strategy (Consensus)

**Source of Truth:** `constitution.md` (human-readable Markdown)
**Machine Artifact:** `rules.yaml` or `governance.lock` (generated)

### 2.2 Constitution Format (GPT-5.2 Proposal)

Embed structured rule blocks in Markdown using fenced YAML:

```markdown
## Rule: No Secrets
Severity: error

\`\`\`codemonkeys-rule
id: "gov.no_secrets"
severity: "error"
check:
  kind: "secret_scan"
  patterns:
    - "AKIA[0-9A-Z]{16}"
    - "-----BEGIN (RSA|EC) PRIVATE KEY-----"
message: "Possible secret committed. Remove and rotate."
\`\`\`
```

### 2.3 Rule Categories (Merged)

| Rule ID | Human Rule | Tool | Severity |
|---------|------------|------|----------|
| `SEC-01` | No Secrets | `gitleaks`, regex | Error |
| `RUST-01` | No `unwrap()` in prod | Semgrep/Clippy | Error |
| `RUST-02` | `unsafe` requires `// SAFETY:` | Tree-sitter | Error |
| `TST-01` | Test coverage > 80% | `cargo-tarpaulin` | Warning |
| `QUAL-01` | Functions < 80 lines | Metrics | Warning |

### 2.4 Warnings vs Errors

| Severity | Behavior | Exit Code |
|----------|----------|-----------|
| **Error** | Hard block (PR cannot merge) | `1` |
| **Warning** | Logged, allows proceed with `--force` | `0` |

---

## 3. Chaos Monkey (Fuzzer Design)

### 3.1 Three Fuzzing Lanes (GPT-5.2)

| Lane | Target | Tool | Best For |
|------|--------|------|----------|
| **CLI** | Binary arguments | Custom harness | CLI tools |
| **HTTP** | API endpoints | Black-box HTTP | Web servers |
| **Function** | Rust functions | `cargo-fuzz` | Libraries |

### 3.2 Input Generation (Gemini)

**Level 1: Drunken Monkey (Inputs)**
- Generate edge cases: `u32::MAX`, `""`, `"\0"`, `"🐒"`
- Use `proptest` for property-based testing

**Level 2: Saboteur (Faults)**
- Inject latency (5000ms on `reqwest`)
- Simulate disk full, permission denied

### 3.3 Crash Detection (Consensus)

| Outcome | Signal | Verdict |
|---------|--------|---------|
| Panic | Exit code `101` | **CRITICAL** |
| Timeout | > budget | **Performance Bug** |
| Error | `Result::Err` | Handled (OK) |
| Success | `200 OK` | Miss |

### 3.4 Safety Rails (All AIs)

1. **Sandbox:** Run in `.codemonkeys/sandbox/` (temp dir)
2. **Network Off:** Default `localhost` only
3. **Credential Scrub:** Clear `AWS_*`, `GITHUB_TOKEN`
4. **Filesystem Deny:** Refuse `/`, `~/.ssh`, `~/.aws`
5. **Resource Caps:** Max runtime, max file size

---

## 4. Banana Economy (Rate Limiting)

### 4.1 Budget System (Consensus)

**1 Banana ≈ 1 unit of work**

| Action | Cost |
|--------|------|
| LLM call | 10-15 🍌 |
| `cargo test` | 3-10 🍌 |
| `cargo build` | 5-6 🍌 |
| Fuzz minute | 5-8 🍌 |

**Default Budget:** 100 🍌 per run

### 4.2 Infinite Loop Prevention

1. **Max Iterations:** `heal: 8`, `chaos: 3`
2. **Exponential Backoff:** Cost increases per retry
3. **Signature Hashing:** Detect same error repeating

### 4.3 Escalation Path

When budget exhausted:
1. **Fail** (default): Exit with artifacts
2. **Ask Human** (`--interactive`): Prompt for more 🍌
3. **Downgrade** (`--degrade`): Skip LLM, run only smoke tests

### 4.4 Example Output (Gemini)

```
🍌 Bankruptcy! The Troop is taking a nap.
Budget remaining: 0 bananas (spent: 100)
Stopped after 5 iterations. Last error: tests failing in auth::token

Next actions:
  [A] Give 20 more 🍌 (retry)
  [B] Downgrade to 'WontFix'
  [C] Show me the error (Human intervention)
```

---

## 5. New Agents (Wild Cards)

### 5.1 Foreman (Planner) — All AIs

**Role:** Breaks intent into executable tickets.

```bash
codemonkeys plan "Add OAuth login with PKCE"
```

**Output:** `.codemonkeys/plan.yaml`
```yaml
tickets:
  - id: T1
    kind: "code"
    description: "Add OAuth PKCE flow module"
  - id: T2
    kind: "tests"
    description: "Add integration test for callback"
  - id: T3
    kind: "chaos"
    description: "Fuzz redirect URI parser"
```

### 5.2 Scout (Reconnaissance) — Grok

**Role:** Analyzes existing codebases, infers domain, suggests rules.

```bash
codemonkeys scout ./my-repo
```

**Output:**
```
Scout Report:
- Domain: Web API (detected handlers, HTTP crates)
- Risk: Missing auth tests
- Suggested Rules:
  - "No direct DB access in handlers" (error)
```

---

## 6. Tech Stack (Finalized)

| Component | Choice |
|-----------|--------|
| Language | Rust |
| CLI | `clap` |
| Config | `.codemonkeys/config.yaml` |
| Fuzzing | `cargo-fuzz`, `proptest` |
| Parsing | `tree-sitter`, `pulldown-cmark` |
| Sandbox | `tempfile`, `bwrap` (optional) |

---

## 7. CLI Commands (v0.1)

```bash
codemonkeys init              # Setup .codemonkeys/
codemonkeys check             # Run Silverback governance
codemonkeys check --compile   # Generate rules.yaml from constitution.md
codemonkeys heal              # Run Code Monkey to fix errors
codemonkeys chaos --lane cli  # Run Chaos Monkey (CLI lane)
codemonkeys chaos --lane http # Run Chaos Monkey (HTTP lane)
codemonkeys status            # Show Observer memory
codemonkeys plan "Add X"      # Run Foreman planner
codemonkeys scout ./repo      # Run Scout reconnaissance
codemonkeys replay <run_id>   # Replay a previous run (determinism)
```

---

## 8. Next Steps

| Priority | Task | Owner |
|----------|------|-------|
| **P0** | Create `constitution.md` with `codemonkeys-rule` blocks | Human |
| **P0** | Implement `codemonkeys check` (Silverback) | Code |
| **P1** | Implement `codemonkeys chaos --lane cli` | Code |
| **P1** | Implement Banana Economy ledger | Code |
| **P2** | Implement `codemonkeys plan` (Foreman) | Code |
| **P2** | Implement `codemonkeys scout` | Code |
