# Master Backlog (Code Monkeys)

**Doc Owner (Admin):** Nexus Agent  
**Governance Owner (Approval):** Human Operator  
**Status:** Active  
**Last Updated:** 2025-12-21

## How to Read This Backlog

- **Epics** are outcome-oriented and must include acceptance proofs + evidence hooks.
- **Owners**: Nexus administers work; Human approves governance changes; Code Monkeys execute.
- **Definition of Done** always includes: tests + evidence artifacts + schema validity + Dash visibility.

---

## EPIC-000: Governance as Code (Constitution-Centric Control)

**Goal:** Constitution + Autonomy Governance become machine-checkable gates.  
**Why:** prevents drift and bypass.

### Stories
- **ST-0001**: Governed Docs Registry
  - Add `docs/pm/GOVERNED_DOCS.md` listing canonical docs, owners, approval rules, versioning rules.
  - **Acceptance Proof:** Silverback validates governed docs exist and match required header fields.
  - **Evidence:** Silverback log + CI artifact.

- **ST-0002**: Constitution Compliance Checks (Bootstrap)
  - Silverback checks that specs explicitly declare: constraints, budgets, evidence, traceability.
  - **Acceptance Proof:** failing spec blocks merge; passing spec passes CI.
  - **Evidence:** CI run logs.

- **ST-0003**: Constitution Refactor (Universal + Appendices)
  - Break monolith into: Universal + Code Monkeys + Science Monkeys + Nexus appendices.
  - **Acceptance Proof:** docs compile/validate; references updated; no broken links.
  - **Evidence:** PR + CI artifacts.

---

## EPIC-001: Design Dossier Intake Pipeline (Upstream of Specs)

**Goal:** Design Dossier drives spec creation under Constitution.  
**Why:** Science→Code becomes real.

### Stories
- **ST-0011**: Design Dossier Template Enforcement
  - Ensure dossier contains hypothesis, experiments, MVP boundary, acceptance proofs.
  - **Acceptance Proof:** dossier missing acceptance proofs triggers Nexus escalation request.
  - **Evidence:** generated request artifact in nexus/inbox.

- **ST-0012**: Dossier → Spec Skeleton Generator (Bootstrap)
  - Tool generates spec scaffolding from dossier fields + constitutional required sections.
  - **Acceptance Proof:** generated spec passes Silverback mandatory section check.
  - **Evidence:** generated spec + Silverback output.

---

## EPIC-002: Factory CLI (Control Plane)

**Goal:** One interface: humans + agents run the factory the same way.

### Stories
- **ST-0021**: `codemonkeys run <product>`
  - Runs tests, generates run report, validates schema, updates Dash artifacts.
  - **Acceptance Proof:** last_run.json updated + schema valid + Dash reflects new state.
  - **Evidence:** last_run.json + pytest_output.log + CI artifacts.

- **ST-0022**: `codemonkeys silverback --all`
  - Wrapper for validations.
  - **Acceptance Proof:** exits non-zero on violations; CI blocks.
  - **Evidence:** silverback_output.log

- **ST-0023**: `codemonkeys nexus exec`
  - Wrapper for decision execution with dry-run support.
  - **Acceptance Proof:** decision marked executed + audited artifact generated.
  - **Evidence:** updated decision artifact + audit log.

---

## EPIC-003: PR Wave + Ship System

**Goal:** manufacturing releases becomes repeatable and safe.

### Stories
- **ST-0031**: PR Wave Contract
  - Define max PRs per wave, label gating, retry rules.
  - **Acceptance Proof:** CI enforces PR wave rules (bootstrap: documentation check).
  - **Evidence:** CI log.

- **ST-0032**: Release Artifacts
  - Generate changelog + release notes as mandatory evidence.
  - **Acceptance Proof:** release PR fails if release notes missing.
  - **Evidence:** release notes artifact + CI log.

---

## EPIC-004: Fleet Operations

**Goal:** operate 20+ products without manual tracking.

### Stories
- **ST-0041**: Stale Artifact Detection
  - Flag products with old last_run.
  - **Acceptance Proof:** Dash shows stale badge; Silverback warning.
  - **Evidence:** Dash screenshot + artifact.

- **ST-0042**: Fleet Health Summary Artifact
  - Generate `dash/fleet_health.json`
  - **Acceptance Proof:** schema valid; Dash displays rollup.
  - **Evidence:** fleet_health.json + CI.

---

## EPIC-005: Codebase Oracle (Deterministic Scan + Context Pack)

**Goal:** scalable context retrieval and resumability.

### Stories
- **ST-0051**: Deterministic Scan Hash
- **ST-0052**: Context Pack Generator (for fresh AI instances)
- **ST-0053**: Scan verification in CI (optional)

---

## EPIC-006: Self-Healing CI (Bounded)

**Goal:** bounded repair attempts that cannot modify forbidden areas.

### Stories
- **ST-0061**: Healing attempt budget + stop rules
- **ST-0062**: Structured error feed (anti-prompt-injection)
- **ST-0063**: Repair evidence artifact pack

---

## Immediate Next Up (Backlog)

1. EPIC-000 ST-0001 (Governed Docs Registry)
2. EPIC-002 ST-0021/22/23 (Factory CLI spine)
3. EPIC-001 ST-0012 (Dossier → Spec skeleton)
