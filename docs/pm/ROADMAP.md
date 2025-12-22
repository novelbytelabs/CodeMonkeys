# Code Monkeys Roadmap

**Doc Owner (Admin):** Nexus Agent  
**Governance Owner (Approval):** Human Operator  
**Applies to:** Code Monkeys + Science Monkeys + Dash + Nexus + Silverback  
**Status:** Active  
**Last Updated:** 2025-12-21

## 0. North Star

Build a **local-first autonomous software production factory** where the Human defines:
- vision + constitutional constraints + high-level intent
…and the system manufactures:
- specs, plans, tasks, code, tests, evidence, PR waves, releases, and operational status
with **bounded autonomy**, **non-bypassable governance**, and **evidence-first truth**.

## 1. Authority Chain (Non-Negotiable)

**Design Dossier + Constitution > Spec**

1. **Constitution** (supreme law; non-bypassable)
2. **Design Dossier** (why/what, experiments, acceptance proofs)
3. **Spec** (implementation contract derived from dossier under constitution)
4. **Plan / Tasks** (execution decomposition)
5. **Evidence Pack + Artifacts** (truth layer)
6. **Dash** (operating console)
7. **Nexus queue** (decisions + escalations)

## 2. Current State (v0.2.1 Foundation)

**Foundation is real and working:**
- Dash reads per-product run artifacts
- Schemas exist and are validated
- Silverback validates Specs + Artifacts + Nexus inbox/outbox
- CI enforces tests + Silverback + artifact generation
- Nexus has inbox/outbox + decision executor
- Fleet exists (multiple products tracked)
- Branching workflow (main/dev/feature/*) operational
- Vision + decision log + boot prompt exist (anti-context-loss)

## 3. Strategic Pillars

1. **Governance First**
   - Constitution and Autonomy Governance are enforceable and non-bypassable.
2. **Evidence First**
   - Claims require artifacts. Artifacts are schema-valid.
3. **Local First**
   - No cloud dependency required to run the factory.
4. **Fleet First**
   - System scales across many products without manual babysitting.
5. **Bounded Autonomy**
   - Budgets + stop rules + kill switch always apply.

## 4. Milestones

### M1 — v0.2.x “Foundation Hardening”
**Goal:** tighten correctness + remove bootstrap shortcuts while keeping velocity.
- Branch protection fully enabled (dev/main)
- Warning policy formalized (dev warnings ok; main warnings fail)
- Spec readiness: mandatory sections non-empty for merge to main
- Dash: fleet status is reliable and clear

### M2 — v0.3 “Factory Control Plane”
**Goal:** one official interface that agents + humans use.
- `codemonkeys` CLI wraps all factory operations
- CLI becomes the CI entrypoint (not ad-hoc scripts)
- Fleet commands: list/register/status/run
- Nexus commands: validate/exec/escalate

### M3 — v0.4 “Ship System”
**Goal:** PR wave + release manufacturing becomes routine.
- PR wave policy enforced (max PRs per wave, label gating)
- Release artifacts (changelog + release notes) become mandatory evidence
- Dash displays last release + release evidence links

### M4 — v0.5 “Codebase Oracle”
**Goal:** deterministic local indexing + context pack generation.
- `codemonkeys scan` generates deterministic graph + hash
- Context packs for fresh model instances
- “Resume protocol” validated end-to-end

### M5 — v0.6 “Self-Healing CI”
**Goal:** bounded auto-repair that cannot jailbreak governance.
- max attempts enforced
- structured error feed only
- forbidden paths protected (workflows, secrets, manifests)
- healing produces evidence artifacts

### M6 — v0.7 “Science → Code Handoff Online”
**Goal:** Science Monkeys generate Design Dossiers that Code Monkeys can manufacture into products.
- Dossier intake creates spec skeleton + acceptance proofs
- Dash shows dossier-driven product pipeline state

## 5. Release Discipline

- `dev` = integration branch (CI required)
- `main` = stable release branch (PR required + CI required + stricter policy)
- All major changes occur on `feature/*` branches → PR → `dev` → release PR → `main`

## 6. Open Decisions (Tracked in docs/pm/DECISIONS.md)

- Warning policy (dev vs main)
- Constitution refactor strategy (universal vs appendices)
- When to flip from “bootstrap evidence allowed” to “production evidence required”
