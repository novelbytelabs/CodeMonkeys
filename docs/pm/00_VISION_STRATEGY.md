# Code Monkeys — Vision & Strategy

**Doc ID**: PM-00  
**Status**: Canonical  
**Version**: 0.1  
**Last Updated**: 2025-12-21  
**Owner**: Human Operator (governance author)  
**Applies to**: Nexus Agent, Code Monkeys, Science Monkeys, Antigravity AI repo manager

---

## 1) Vision (What we are building)

**Code Monkeys is an autonomous software production factory** that enables a solo operator to build, ship, and maintain a *portfolio* of products from one workstation by owning only the highest-leverage inputs:

- intent + constraints + acceptance proofs
- governance/constitution
- portfolio prioritization (budgets, timing, what matters most)

Everything else is delegated to an agent swarm operating under enforceable rules (tests, evidence, budgets, CI gates).

**End state:** a single operator can sustainably maintain 20+ products (and more later) without daily manual intervention across the whole portfolio.

---

## 2) Strategy (How we win)

We win by turning "software development" into a **repeatable manufacturing loop**:

**Spec → Plan → Tasks → Implement → Verify → Evidence Artifacts → Dash → Silverback → CI → Nexus**

Key idea: *software progress is only recognized through artifacts + proofs*, not narration.

---

## 3) What the Human Owns (and what the system owns)

### Human Operator owns (non-delegable)
1. **Governance authoring**  
   - constitution & autonomy rules
   - policy on budgets, safety, evidence requirements
2. **Portfolio priorities**  
   - what gets built next, what gets paused, what ships
3. **Final overrides / kill-switch authority**
4. **Definition of "DONE"**  
   - acceptance criteria and evidence requirements

### Nexus Agent owns (within governance)
- product-level executive decisions
- budget allocation proposals
- escalation routing
- maintenance scheduling and prioritization

### Science Monkeys own (future / currently offline)
- discovery and R&D
- hypotheses → experiments → results
- creation of Design Dossiers for handoff

### Code Monkeys own
- implementation + tests + docs + CI compliance
- producing artifacts that prove correctness
- operating within budgets and stop rules

### Silverback owns
- enforcement (spec readiness, artifact validity, evidence presence, governance compliance)
- stopping the line when rules are violated

### Antigravity AI (Repo Manager) owns
- keeping canonical docs updated
- integrating architectural deltas into master docs
- maintaining templates and ensuring process consistency

---

## 4) Strategic Pillars (What drives our decisions)

### Pillar A — Governance First (Non-bypassable rules)
- Constitution and Autonomy Governance are not "guidelines"; they are merge/ship gates.
- Governance must be **executable** (validators + CI), not only prose.

### Pillar B — Evidence First (No evidence = not true)
- Every claim must be backed by artifacts: logs, reports, schema-valid JSON, screenshots (bootstrap), CI outputs.
- Dash is the evidence viewer; artifacts are the source of truth.

### Pillar C — Local First (Solo workstation control)
- The system must run locally, be reproducible, and avoid hidden cloud dependencies by default.
- CI is the enforcement surface; development is local.

### Pillar D — Portfolio Scale (Fleet thinking)
- Dash must support many products.
- Work is scheduled, prioritized, and budgeted across the fleet (banana economy).

### Pillar E — Stop Rules & Budgets (Bounded autonomy)
- Autonomy must stop on budget exhaustion, repeated failures, scope creep, or kill switch.
- "Continuing anyway" is forbidden.

---

## 5) What we are NOT doing (Non-goals)

- Not building a full Kubernetes-style platform.
- Not building a general autonomous AI with unbounded authority.
- Not trusting narration; not accepting "it works" without evidence.
- Not aiming for max sophistication in v0.x—aiming for **repeatable reliability**.

---

## 6) Current Reality (Bootstrap truth)

- The system is in **early development**.
- Many "agents" are currently **documented interfaces**, not live autonomous workers.
- Science Monkeys are **offline**.
- What is real today: Dash + artifact contracts + Silverback validator + CI enforcement + Nexus schema validation + Nexus executor.

---

## 7) Canonical Laws and Contracts (Read-first docs)

These docs define what is true and enforceable:

1. `constitution.md`  
2. `docs/pm/AUTONOMY_GOVERNANCE.md`  
3. `docs/pm/RUN_ARTIFACT_CONTRACT.md`  
4. `docs/agent/CODEMONKEYS_MASTER_ARCHITECTURE.md`  
5. `CONTEXT_SNAPSHOT.md`  
6. `.specify/templates/spec-template.md` (spec contract)

---

## 8) Roadmap (Strategic milestones)

### Foundation (mostly complete)
- Dash MVP
- Formal schemas + report generator
- Silverback validator
- CI enforcement
- Nexus inbox/outbox schemas + validation
- Nexus executor (budget grants, kill switches)

### Next: Fleet Scale (P8)
- multiple products in `products.json`
- per-product run artifacts and status
- portfolio view in Dash

### Later: Science Monkeys integration (handoff)
- Design Dossier pipeline (Science → Code)
- experiments + notebooks become first-class evidence artifacts

---

## 9) North Star Metrics (How we know we're winning)

- **Time-to-evidence:** median time from spec to schema-valid evidence artifacts
- **Governance compliance rate:** % runs/PRs passing Silverback without warnings/errors
- **CI reliability:** PR pass rate and mean failure resolution time
- **Fleet capacity:** number of products with "active maintenance loop"
- **Operator load:** minutes/day the human must intervene to keep the fleet healthy

---

## 10) Decision Rules (If there is conflict…)

1. Constitution > Autonomy Governance > Spec > Plan > Tasks > Code.
2. If it isn't enforceable, it isn't governance.
3. If it isn't testable, it isn't a requirement.
4. If it isn't evidenced, it isn't done.
5. If it isn't bounded, it isn't allowed.

---

## 11) Resume Protocol (for new model instances)

When restarting a new ChatGPT instance, provide:
- `CONTEXT_SNAPSHOT.md`
- this file `docs/pm/00_VISION_STRATEGY.md`
- latest commit hashes for `main` and `dev`
- current active feature branch + PR link
- the specific next milestone (e.g., P8 Fleet Expansion)

**Boot prompt for a new instance:**
> You are the PM for Code Monkeys. Read `docs/pm/00_VISION_STRATEGY.md` and `CONTEXT_SNAPSHOT.md` first. Your job is to protect governance-first, evidence-first development and coordinate Antigravity AI. Assume early bootstrap stage; prefer executable enforcement (tests, schemas, CI). Propose the next smallest shippable milestone and the acceptance proofs.
