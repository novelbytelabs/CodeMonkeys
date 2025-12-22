# CodeMonkeys: Master Architecture

> *"A software automation platform that permits a single entrepreneur to build and manage 50+ software products using one CLI on one computer locally."*

---

## The DevSecOps Loop

**Security is not an afterthought — it is a design element.**

**Dev = DevSec** | **Ship = Ops** → Complete **DevSecOps**

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                           THE COMPLETE DEVSECOPS LOOP                        │
│                                                                              │
│   ┌─────────┐   ┌──────────────────────────────────────────────┐   ┌───────┐ │
│   │  INIT   │ → │  DEV (DevSec)                                │ → │ SHIP  │ │
│   │         │   │                                              │   │ (Ops) │ │
│   │ Scaffold│   │ Constitution → Spec → Plan → Tasks →         │   │       │ │
│   │ Onboard │   │ Analysis → Implement → Secure → Test         │   │ Heal  │ │
│   │ Gap Fix │   │                                              │   │ Docs  │ │
│   └─────────┘   └──────────────────────────────────────────────┘   │Release│ │
│                                                                    │Publish│ │
│       ↓                           ↓                                │Announce││
│   "Make it               "Make it work"                            │Monitor│ │
│    exist"                "Make it safe"                            └───────┘ │
│                                                                       ↓      │
│                                                              "Make it live"  │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## The Three Pillars

```
┌────────────────────────────────────────────────────────────────┐
│                      CODEMONKEYS                               │
│                                                                │
│   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐          │
│   │    INIT     │   │     DEV     │   │    SHIP     │          │
│   │             │   │             │   │             │          │
│   │  Scaffold   │   │   DevSec    │   │    Ops      │          │
│   │  Onboard    │   │   Coding    │   │   Release   │          │
│   │  Gap Fix    │   │   Security  │   │   Publish   │          │
│   └─────────────┘   └─────────────┘   └─────────────┘          │
│                                                                │
│        ↓                  ↓                  ↓                 │
│   "Make it exist"   "Make it work"    "Make it live"           │
│                      "Make it safe"                            │
└────────────────────────────────────────────────────────────────┘
```

---

# PILLAR 1: INIT

**Goal:** Make it exist (new or existing project).

## Commands

```bash
codemonkeys init                      # Interactive wizard
codemonkeys init --template rust      # New project from template
codemonkeys init .                    # Onboard existing project
codemonkeys init --analyze            # Gap analysis (dry run)
```

## Features

| Feature | Description |
|---------|-------------|
| **Templates** | Rust, Python, TypeScript, Go, C |
| **Onboarding** | Analyze existing repo, identify gaps |
| **Gap Analysis** | What's missing vs. CodeMonkeys requirements? |
| **Auto-Fix** | Install/configure missing components |
| **AI Checklist** | Interactive wizard with memory |

## What Gets Created

```
.codemonkeys/
├── config.yaml           # Project config
├── constitution.md       # Governance rules
└── runs/                 # Run artifacts (gitignored)
```

---

# PILLAR 2: DEV (DevSec)

**Goal:** Make it work. Make it safe.

**Heritage:** Fork/merge of Spec-Kit + Google Conductor ideas.

## The Full Dev Loop

```
┌──────────────────────────────────────────────────────────────┐
│                        DEV LOOP                              │
│                                                              │
│   1. Constitution  →  Define the laws (what NOT to do)       │
│   2. Spec          →  Define the intent (what TO do)         │
│   3. Plan          →  Architecture & design decisions        │
│   4. Tasks         →  Break down into tickets (T1, T2...)    │
│   5. Analysis      →  Review plan, identify risks            │
│   6. Implement     →  Write code (Code Monkey)               │
│   7. Secure        →  Security checks (NOT OPTIONAL)         │
│   8. Test          →  Verify correctness (Chaos Monkey)      │
│                                                              │
│   Loop until all tasks complete.                             │
└──────────────────────────────────────────────────────────────┘
```

## Commands

```bash
codemonkeys dev                       # Full loop
codemonkeys dev constitution          # Create/update Constitution
codemonkeys dev spec "Add OAuth"      # Create specification
codemonkeys dev clarify               # Clarify underspecified areas
codemonkeys dev plan                  # Generate architecture plan
codemonkeys dev tasks                 # Break into tickets
codemonkeys dev taskstoissues         # Convert tasks to GitHub issues
codemonkeys dev analyze               # Cross-artifact consistency check
codemonkeys dev checklist             # Generate custom checklist
codemonkeys dev implement             # Code generation
codemonkeys dev secure                # Security scan + fixes
codemonkeys dev test                  # Run tests + chaos
```

## The Troop (Agents)

| Agent | Role | Phase |
|-------|------|-------|
| 🦍 **Silverback** | Governance enforcement | Constitution, Secure |
| 🐒 **Code Monkey** | Builder, fixer | Implement |
| 🦧 **Foreman** | Planner, ticket breaker | Plan, Tasks |
| 🐵 **Chaos Monkey** | Fuzzer, adversary | Test |
| 🐵 **Scout** | Reconnaissance | Analysis |
| 🔒 **Security Monkey** | Security specialist | **Secure** |

## Security (Baked In)

| Check | Tool/Method |
|-------|-------------|
| **Secret Scan** | gitleaks, builtin regex |
| **Dependency Audit** | cargo-audit, npm audit, pip-audit |
| **SAST** | Semgrep, CodeQL |
| **License Compliance** | cargo-deny, etc. |
| **Unsafe Code** | Rust unsafe audit, memory safety |
| **OWASP Top 10** | Web security checks |

---

# PILLAR 3: SHIP (Ops)

**Goal:** Make it live.

**Heritage:** The full Code Monkeys vision.

## The Ship Pillars (from Code Monkeys)

```
┌──────────────────────────────────────────────────────────────┐
│                        SHIP PILLARS                          │
│                                                              │
│   1. Documentation  →  Auto-generate docs, API refs          │
│   2. CI/CD          →  Setup GitHub Actions, pipelines       │
│   3. PR/Merge       →  Create PRs, governance checks         │
│   4. Website        →  Landing page, docs site               │
│   5. Publish        →  crates.io, npm, PyPI, Docker          │
│   6. Release Notes  →  Changelog, version bumps              │
│   7. Monitoring     →  Health checks, alerting               │
└──────────────────────────────────────────────────────────────┘
```

## Commands

```bash
codemonkeys ship                      # Full release pipeline
codemonkeys ship docs                 # Generate documentation
codemonkeys ship ci                   # Setup/update CI/CD
codemonkeys ship pr                   # Create PR with governance
codemonkeys ship website              # Generate website
codemonkeys ship publish              # Publish to registries
codemonkeys ship release              # Version bump + changelog
codemonkeys ship monitor              # Setup monitoring
```

---

# The 50+ Projects Scale

## Fleet Management

```bash
codemonkeys status                    # Single project
codemonkeys status --all              # All 50+ projects
codemonkeys fleet                     # Fleet dashboard
codemonkeys fleet prioritize          # Which project needs attention?
```

## Cross-Project Memory

- Learn from fixes in Project A, apply to Project B  
- Shared Constitution templates  
- Unified security policies  

---

# Banana Economy (Resource Management)

| Resource | Budget Per Run |
|----------|----------------|
| Wall-clock time | 900 seconds |
| Test runs | 6 |
| LLM calls | 4 |
| Security scans | 3 |

**Prevents:** Infinite loops, runaway costs.  
**Enables:** Autonomous operation within bounds.  

---

# CLI Summary

```bash
# INIT — Make it exist
codemonkeys init [--template <lang>] [path]

# DEV — Make it work, make it safe
codemonkeys dev [constitution|spec|plan|tasks|analyze|implement|secure|test]

# SHIP — Make it live
codemonkeys ship [docs|ci|pr|website|publish|release|monitor]

# META
codemonkeys status [--all]
codemonkeys fleet
codemonkeys --tui
```

---

# Ideas to Preserve

## From Code Monkeys
- Living Linter (rule evolution)
- Adaptive Immunity (auto-fix propagation)
- Reality Forks (canary branching)
- Adversarial Justice (LLM vs LLM)

## From Spec-Kit
- `/speckit.specify` → `codemonkeys dev spec`
- `/speckit.plan` → `codemonkeys dev plan`
- `/speckit.tasks` → `codemonkeys dev tasks`
- `/speckit.implement` → `codemonkeys dev implement`

## From AI Collaboration (Gemini, Grok, GPT)
- Foreman (Planner agent)
- Scout (Reconnaissance agent)
- Security Monkey (Agent for Secure phase)
- Multi-wallet Banana Economy
- governance.lock with hashes
- RunReport artifact format

---

# Roadmap

## v0.1 — Foundation
- [ ] `codemonkeys init` (basic scaffolding)
- [ ] `codemonkeys dev constitution` (governance)
- [ ] `codemonkeys dev implement` (Code Monkey)
- [ ] `codemonkeys dev secure` (basic security scans)

## v0.2 — Dev Loop Complete
- [ ] `codemonkeys dev spec/plan/tasks`
- [ ] `codemonkeys dev test` (Chaos Monkey)
- [ ] `codemonkeys dev analyze` (Scout)

## v0.3 — Ship Pillars
- [ ] `codemonkeys ship docs`
- [ ] `codemonkeys ship ci`
- [ ] `codemonkeys ship pr`

## v1.0 — Full Platform
- [ ] Fleet management (50+ projects)
- [ ] The ZooKeeper (optional GUI)
- [ ] Cross-project memory

---

**Version:** 2.0.0
**Date:** 2025-12-20
**Status:** APPROVED VISION
