# CodeMonkeys: Complete Feature Mapping

> Synthesized from all docs/ and .agent/ documentation.
> Code Monkeys becomes `codemonkeys ship`.

---

## PILLAR 1: INIT (Bootstrap)

**Goal:** 0 → Working Repository with Full CI/CD Wiring

### From Existing Docs:
| Source | Feature | Notes |
|--------|---------|-------|
| VISION.md | CodeMonkeysInit | "0 → working repo with CI/release wiring" |
| docs/index.md | `codemonkeys init` | Creates `.codemonkeys/` + config |
| configuration.md | Default templates | Rust/Python/Full-stack configs |

### Features for `codemonkeys init`:
- [ ] **Project Templates:** Rust, Python, TypeScript, Go, C
- [ ] **Onboarding Wizard:** AI-assisted gap analysis
- [ ] **Constitution Scaffold:** Default rules + machine-parseable blocks
- [ ] **Config Generation:** `.codemonkeys/config.yaml`
- [ ] **CI Wiring:** GitHub Actions for check/heal/ship
- [ ] **Fleet Registration:** Connect to ZooKeeper (future)

---

## PILLAR 2: DEV (DevSec)

**Goal:** Spec → Plan → Tasks → Analysis → Implement → SECURE → Test

### From Existing Docs:
| Source | Feature | Maps To |
|--------|---------|---------|
| VISION.md | CodeMonkeysDev | "Spec → Plan → Tasks → Tests (SDD+TDD)" |
| MOONSHOT_IDEAS.md | Adversarial Justice LLM | `dev secure` |
| MOONSHOT_IDEAS.md | Living Knowledge Graph | `dev analyze` |
| architecture.md | Oracle Module | `dev analyze` (code understanding) |
| architecture.md | Heal Module | `dev implement` + `dev test` |
| ORCHESTRATOR_ARCHITECTURE.md | Worker/Scanner | `dev implement` |
| ADAPTIVE_IMMUNITY.md | Living Linter | `dev secure` |

### The Full Dev Loop:

```
Constitution → Spec → Plan → Tasks → Analysis → Implement → SECURE → Test
     ↑          ↑       ↑       ↑        ↑          ↑          ↑        ↑
Silverback  Foreman  Foreman  Foreman  Scout   CodeMonkey  Security  Chaos
```

### Features for `codemonkeys dev`:

#### `codemonkeys dev constitution`
- [ ] Parse/validate Constitution
- [ ] Compile governance.lock
- [ ] Justice LLM review (optional)

#### `codemonkeys dev spec "description"`
- [ ] Natural language → structured spec
- [ ] Spec-Kit integration (clarify workflow)
- [ ] Traceability matrix setup

#### `codemonkeys dev plan`
- [ ] Architecture design from spec
- [ ] PlanSpec v1 generation
- [ ] Silverback validation (scope, risk)

#### `codemonkeys dev tasks`
- [ ] Break plan into tickets (T1, T2, ...)
- [ ] Dependency ordering
- [ ] Budget estimation

#### `codemonkeys dev analyze`
- [ ] Oracle module (code graph + vectors)
- [ ] Living Knowledge Graph queries
- [ ] Risk identification (Scout agent)

#### `codemonkeys dev implement`
- [ ] Code Monkey agent
- [ ] Max iterations (default 3)
- [ ] Whole-block replacement (Constitution XVII.3)
- [ ] Scope enforcement (write_allowlist/denylist)

#### `codemonkeys dev secure`
- [ ] Secret scan (gitleaks, builtin regex)
- [ ] Dependency audit (cargo-audit, pip-audit)
- [ ] SAST (Semgrep, CodeQL)
- [ ] License compliance (cargo-deny)
- [ ] Unsafe code audit (Rust)
- [ ] OWASP Top 10 (web apps)
- [ ] Security Monkey agent

#### `codemonkeys dev test`
- [ ] Run tests (cargo test, pytest)
- [ ] Chaos Monkey fuzzing (v0.2)
    - Fuzz lane: CLI, HTTP, Function
    - Proptest (stable), cargo-fuzz (nightly)
- [ ] Synthetic User Swarms (v0.3)
    - Headless browser agents
    - Distinct personas ("The Hacker", "The Power User")

---

## PILLAR 3: SHIP (Ops)

**Goal:** Governed Releases + Full Deployment Automation

### From Existing Docs:
| Source | Feature | Maps To |
|--------|---------|---------|
| VISION.md | Code Monkeys | "Heal → Docs → Ship → Publish → Announce" |
| architecture.md | Ship Module | `ship release` |
| architecture.md | Oracle | Powers `ship docs` |
| docs/cli-reference.md | `codemonkeys ship` | `codemonkeys ship release` |
| FLEET_ARCHITECTURE.md | CodeMonkeysOrg | `ship fleet` |
| ULTIMATE_ARCHITECTURE.md | Jenkins/Ansible/Terraform | `ship deploy` |
| MOONSHOT_IDEAS.md | Self-Directing Documentary | `ship docs` |
| MOONSHOT_IDEAS.md | Predictive Risk Forecast | `ship analyze` |

### Features for `codemonkeys ship`:

#### `codemonkeys ship docs`
- [ ] Living documentation generation
- [ ] README auto-update from Clap
- [ ] Architecture diagrams from code
- [ ] Self-Directing Documentary Engine (browser screenshots)
- [ ] Doc drift detection (Intent vs Implementation)

#### `codemonkeys ship ci`
- [ ] GitHub Actions setup
- [ ] Jenkins integration (self-hosted)
- [ ] Webhook receiver
- [ ] Cron fallback triggers

#### `codemonkeys ship pr`
- [ ] Create governed PR
- [ ] Constitution checks (pre-flight)
- [ ] Canary Ladder (1 → 3 → 10 → Fleet)
- [ ] Auto-merge with governance gates

#### `codemonkeys ship release`
- [ ] SemVer calculation from commits
- [ ] Changelog generation
- [ ] Git tagging
- [ ] Pre-flight checks (clean git, tests pass)

#### `codemonkeys ship publish`
- [ ] crates.io
- [ ] PyPI
- [ ] npm
- [ ] Docker Hub
- [ ] Ansible playbooks for each registry

#### `codemonkeys ship website`
- [ ] Landing page generation
- [ ] MkDocs site
- [ ] Marketing copy auto-generation

#### `codemonkeys ship monitor`
- [ ] Health checks
- [ ] Alerting setup
- [ ] Watch mode daemon

#### `codemonkeys ship announce`
- [ ] Release notes generation
- [ ] Social media automation (Twitter via browser)
- [ ] Email newsletters

---

## CROSS-CUTTING FEATURES

### Fleet Management (`codemonkeys fleet`)
From: FLEET_ARCHITECTURE.md, ORCHESTRATOR_ARCHITECTURE.md

- [ ] `fleet status` — All 50+ projects health
- [ ] `fleet prioritize` — Which needs attention?
- [ ] `fleet apply` — Cross-repo operations
- [ ] Swarm DB — Shared memory across fleet
- [ ] Canary Ladder — Safe rollout (1 → 3 → 10 → all)

### Banana Economy (Resource Management)
From: CODEMONKEYS_ARCHITECTURE_v2.md

- [ ] Multi-wallet: time, tests, builds, LLM calls
- [ ] Ledger persistence
- [ ] Budget enforcement
- [ ] Stopping rules (no-progress, scope-creep)

### The Troop (Agents)
| Agent | Role | Pillar |
|-------|------|--------|
| 🦍 Silverback | Governance | All |
| 🐒 Code Monkey | Builder | DEV |
| 🦧 Foreman | Planner | DEV |
| 🐵 Chaos Monkey | Fuzzer | DEV (v0.2) |
| 🐵 Scout | Reconnaissance | DEV |
| 🔒 Security Monkey | Security | DEV (NEW) |

---

## MOONSHOT IDEAS (Preserved)

### Phase 1 (Near-term):
- [ ] Adversarial Justice LLM (Builder vs Justice)
- [ ] Adaptive Immunity (PR waves, not patches)
- [ ] Living Knowledge Graph
- [ ] Root-Cause Memory

### Phase 2 (Mid-term):
- [ ] Reality Forks (ephemeral test environments)
- [ ] Ouroboros Red Team (self-attack)
- [ ] Visual Turing Test (Vision LLM)
- [ ] Synthetic User Swarms

### Phase 3 (Far-term):
- [ ] Self-Amending Constitution
- [ ] Stigmergic Pipelines (digital pheromones)
- [ ] Morphogenic Code-Sharing Guilds
- [ ] Intent-Based Swarm Collapse
- [ ] Holographic Shadow Corp

---

## CLI COMMAND SUMMARY

```bash
# INIT — Make it exist
codemonkeys init [--template <lang>] [path]
codemonkeys init --analyze              # Gap analysis only

# DEV — Make it work, make it safe
codemonkeys dev                         # Full loop
codemonkeys dev constitution            # Governance
codemonkeys dev spec "description"      # Specification
codemonkeys dev plan                    # Architecture
codemonkeys dev tasks                   # Ticket breakdown
codemonkeys dev analyze                 # Code understanding
codemonkeys dev implement               # Code generation
codemonkeys dev secure                  # Security checks
codemonkeys dev test                    # Verification

# SHIP — Make it live
codemonkeys ship                        # Full release
codemonkeys ship docs                   # Documentation
codemonkeys ship ci                     # CI/CD setup
codemonkeys ship pr                     # Create PR
codemonkeys ship release                # Version + changelog
codemonkeys ship publish                # Registries
codemonkeys ship website                # Generate site
codemonkeys ship monitor                # Setup monitoring
codemonkeys ship announce               # Social/email

# FLEET — Multi-product management
codemonkeys fleet status [--all]
codemonkeys fleet prioritize
codemonkeys fleet apply "<command>"

# META
codemonkeys status                      # Project health
codemonkeys replay <run_id>             # Reproduce past run
codemonkeys --tui                       # Interactive UI
```

---

**Date:** 2025-12-20
**Status:** COMPLETE FEATURE MAP
