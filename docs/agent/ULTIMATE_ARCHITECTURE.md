# Ultimate Code Monkeys Ship Architecture

## Vision

**One system to rule them all.** Code Monkeys Ship orchestrates Jenkins, Ansible, OpenTofu, and browser automation so you don't have to touch them directly.

You write **Constitution + Spec**. Code Monkeys Ship does everything else.

---

## The Stack

```
┌─────────────────────────────────────────────────────────────┐
│                     CONSTITUTION                            │
│           (Ground truth - machine-parseable policy)         │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                      Code Monkeys  ORG                      │
│   Fleet Management · Swarm Intelligence · Multi-Company     │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                     Code Monkeys  SHIP                      │
│      Oracle · Heal · Docs · Ship · Publish · Announce       │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
   ┌─────────┐           ┌─────────┐           ┌──────────┐
   │ Jenkins │           │ Ansible │           │ OpenTofu │
   │  (CI)   │           │(Config) │           │ (Infra)  │
   └─────────┘           └─────────┘           └──────────┘
        │                     │                     │
        └─────────────────────┴─────────────────────┘
                              │
                    ┌─────────────────┐
                    │     Browser     │
                    │   Automation    │
                    │   (Last-Mile)   │
                    └─────────────────┘
```

---

## Components

### 1. Constitution (Policy Layer)
- Machine-parseable rules
- Defines what's allowed/forbidden
- Gates for every action
- Audit requirements

### 2. Code Monkeys Org (Fleet Layer)
- Manages 50+ products across multiple companies
- Swarm DB (patterns shared across all repos)
- Cross-repo operations
- Dashboard for fleet health

### 3. Code Monkeys Ship (Product Layer)
| Pillar | Integrates With | Job |
|--------|-----------------|-----|
| **Oracle** | Local SQLite + LanceDB | Code understanding |
| **Heal** | Jenkins + Ollama | Self-healing CI |
| **Docs** | Git + MkDocs | Living documentation |
| **Ship** | Ansible + registries | Governed releases |
| **Watch** | Jenkins webhooks | Always-on monitoring |

### 4. Jenkins (CI Layer)
- Self-hosted on your hardware
- Unlimited builds, no rate limits
- Code Monkeys Ship triggers via Jenkins API
- Pipelines defined in Jenkinsfile (per repo)

### 5. Ansible (Config/Deploy Layer)
- Playbooks for every deployment scenario
- Code Monkeys Ship runs `ansible-playbook`
- Manages servers, packages, configs
- Idempotent = safe to run repeatedly

### 6. OpenTofu (Infrastructure Layer)
- Only when you need cloud resources
- Code Monkeys Ship runs `opentofu apply`
- State managed per-product

### 7. Browser Automation (Last-Mile Layer)
- For UIs without APIs
- Screenshots/recordings for audit
- Examples: Twitter, AWS Console, Stripe

---

## Data Flow

```
Event (webhook/cron/manual)
        │
        ▼
   Code Monkeys Ship Watch
        │
        ├──→ Heal needed? ─→ Jenkins (build) ─→ Ollama (fix) ─→ Git (commit)
        │
        ├──→ Docs drift? ─→ Regenerate ─→ Git (PR)
        │
        ├──→ Release ready? ─→ Ansible (deploy) ─→ Registries ─→ Browser (announce)
        │
        └──→ Log to SwarmDB
```

---

## Swarm Intelligence

Each Code Monkeys Ship instance reports to the Swarm DB:

| Data | Use |
|------|-----|
| Error patterns | "I've seen this before" |
| Fix templates | Reuse successful fixes |
| Build times | Predict slowdowns |
| Dep conflicts | Warn before you hit them |

**Result**: Product #50 benefits from lessons learned in products #1-49.

---

## What You Touch vs What Code Monkeys Ship Touches

| You | Code Monkeys Ship |
|-----|-------------------|
| Constitution | Everything else |
| Spec | Jenkinsfiles |
| Tests | Ansible playbooks |
| | OpenTofu configs |
| | Browser scripts |
| | Docs |
| | Releases |

---

## Implementation Phases

### Phase 1: Core (✅ Done)
- Oracle (code graph + search)
- Heal (LLM repair + rollback)
- Ship (semver + changelog)

### Phase 2: Watch & Daemon
- `codemonkeys watch` command
- Webhook receiver OR cron trigger
- Auto-trigger heal/ship

### Phase 3: Jenkins Integration
- `JenkinsBackend` trait
- Trigger builds via API
- Parse build logs for failures

### Phase 4: Ansible Integration
- `AnsibleRunner` for deployments
- Playbook library (crates.io, PyPI, Docker, etc.)
- Secrets management

### Phase 5: Code Monkeys Org
- Fleet registry
- Multi-account auth
- Cross-repo operations
- Dashboard

### Phase 6: Browser Automation
- Playwright/Puppeteer integration
- Workflow macros for common tasks
- Visual verification

---

## Why This Scales

| Challenge | Solution |
|-----------|----------|
| CI limits | Jenkins (self-hosted, unlimited) |
| Deployment complexity | Ansible (declarative, repeatable) |
| Infrastructure | OpenTofu (code-defined) |
| UI-only tasks | Browser automation |
| 50+ products | Code Monkeys Org fleet management |
| Knowledge silos | Swarm DB (cross-product learning) |
| Maintenance burden | Constitution-governed autopilot |

---

## The Dream

```
You: *define Constitution + Spec*
You: *commit*
You: *sleep*

Code Monkeys Ship:
  - Builds in Jenkins
  - Tests pass ✅
  - Docs regenerated
  - Release cut
  - Published to crates.io
  - Announced on Twitter
  - All logged

You: *wake up* → 50 products green
```

**This is the solo product factory at enterprise scale.**
