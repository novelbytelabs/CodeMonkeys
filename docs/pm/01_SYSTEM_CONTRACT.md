# Code Monkeys System Contract (Human ↔ Nexus ↔ Swarms)

Date: 2025-12-21
Status: Draft (v0.1)

This document defines **who is responsible for what and why** in the Code Monkeys ecosystem.

## 1) Entities

### Human (You)
Role: constitutional designer + portfolio supervisor  
Default posture: **not in the loop** for day-to-day operations

### Nexus Agent (Organizational Product Owner)
Role: executive decision-maker and preference model for the human.
Nexus is the **authority** for product decisions unless explicitly restricted by the Constitution.

### Science Monkeys (R&D swarm)
Role: discover and design novel products via scientific investigation loops.

### Code Monkeys (Production swarm)
Role: build/ship/maintain software products using SDD+TDD, CI governance, evidence packs.

## 2) Authority Model

### 2.1 What the Constitution controls (non-negotiable)
The Constitution is the highest authority and applies to **all** agents (including Nexus).

Non-negotiables:
- No fake evidence; claims must be Observed/Derived/Unverified
- Verification gates required (tests/lint/build/security where applicable)
- Bounded autonomy (attempt limits, budgets, circuit breakers)
- No secret leakage; no unsafe scope changes
- Traceability: requirement ↔ code ↔ tests ↔ docs ↔ evidence

### 2.2 Decisions Nexus MAY make autonomously
- Selecting which product ideas to explore (within portfolio budget)
- Approving plans/tasks that conform to Constitution + Spec
- Shipping routine non-breaking releases with green CI + evidence pack
- Scheduling maintenance work (dependency bumps, minor refactors) within scope limits

### 2.3 Decisions that require explicit Human approval (default)
- Creating a new company/org boundary (legal/brand decisions)
- Publishing a paid product / pricing changes
- Any breaking change (SemVer major) to a public API
- Any action that relaxes governance, reduces verification, or changes safety posture
- High-cost actions exceeding defined budgets

**Note:** these can be delegated to Nexus later, but only via explicit constitutional amendment.

## 3) Gates and Stopping Rules (hard safety)

### 3.1 Budget gate (Banana Economy)
All autonomous loops must consume a budget with clear stopping rules.
Example budgets:
- max wall-clock seconds per run
- max CI reruns
- max LLM calls
- max PRs opened per campaign

### 3.2 Verification gate
No merge/release without:
- passing tests/build/lint
- required security scans (configurable)
- evidence pack (logs/artifacts tied to commit/run)

### 3.3 Change-scope gate
Autonomous systems must respect:
- allowed file/path scopes for each action type
- max diff size thresholds
- forbidden changes (CI configs, secret stores, governance files) unless explicitly authorized

### 3.4 Kill switches
- global kill switch (stop all automation)
- per-product kill switch
- per-campaign kill switch (PR wave)

## 4) Mandatory Artifacts

### 4.1 Authoritative (inputs)
- Constitution (single root constitution for Code Monkeys)
- Spec (includes intent, constraints, and acceptance proofs)
- Context Pack (repo map + constraints + dependencies; can be generated but must be referenced)

### 4.2 Derived (outputs)
- Plan (implementation strategy)
- Tasks (dependency-ordered work items)
- Evidence Pack (CI artifacts, test outputs, scan summaries)
- Release Notes / Changelog updates

### 4.3 Science → Code handoff artifact (required for autonomy)
A **Design Dossier / Proof Bundle** must exist before Code Monkeys production starts.
See HANDOFF_CONTRACT.md.

## 5) What "done" means
A feature is done only when acceptance proofs pass and evidence is attached.
If there is no evidence, the claim is false.
