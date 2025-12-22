# CONTEXT SNAPSHOT: Code Monkeys
**Date:** 2025-12-21
**Version:** 0.2 (Bootstrap)

## 0. How to Resume (Start Here)
- **Last Checkpoint**: P7.2 complete (Nexus executor).
- **Current Milestone**: Vision docs + pending PRs.
- **Commit Hashes (main)**:
    - P2: `2c8822f` (Bootstrap MVP)
    - P3: `371806e` (Schemas + report generator)
    - P4: `730fb7f` (Hardened generator + gc_runs)
    - P5: `9dc9b4c` (Governance + Silverback + preflight)
    - P6: `5b51f96` (CI workflow)
    - P6.1+P7: `0fc1c08` (CI hardening + Nexus stubs)
- **Branch Status**:
    - `main`: stable at `0fc1c08`
    - `dev`: `65927f9` (branching workflow)
    - Feature branches pending PR (see below)
- **Feature Branches Pending PR**:
    - `feature/nexus-validation` (P7.1)
    - `feature/fleet-expansion` (P8)
    - `feature/nexus-executor` (P7.2)
    - `feature/vision-docs` (current)
- **Canonical 'Start Here' Files**:
    - `docs/pm/00_VISION_STRATEGY.md` (North star principles)
    - `CONTEXT_SNAPSHOT.md` (This file)
    - `docs/pm/AUTONOMY_GOVERNANCE.md` (Governance rules)
    - `docs/pm/99_AGENT_BOOT_PROMPT.md` (Quick restore)
    - `docs/pm/DECISIONS.md` (Decision log)

## 1. Overview
Code Monkeys is an autonomous software production factory for a solo operator. It consists of:
- **Science Monkeys** (R&D): Discover and design products. (Offline)
- **Code Monkeys** (Production): Build, ship, and maintain products.
- **Nexus Agent**: Organizational Product Owner (Executive decision-maker).
- **Silverback**: Governance enforcement.

The system is "governance-first," prioritizing clear rules, evidence-based claims, and bounded autonomy.

## 2. Authority Model
1. **Constitution**: The highest authority. Non-negotiable rules.
2. **Human (User)**: Portfolio supervisor. Governance designer.
3. **Nexus Agent**: Product Owner. Makes autonomous decisions within bounds.
4. **Swarms**: Execution engines. Bound by Spec and Constitution.

## 3. Canonical Documentation
| Doc | Purpose | Location |
|---|---|---|
| **Vision & Strategy** | North star principles | `docs/pm/00_VISION_STRATEGY.md` |
| **System Contract** | Roles & Responsibilities | `docs/pm/01_SYSTEM_CONTRACT.md` |
| **Autonomy Governance** | Enforceable rules | `docs/pm/AUTONOMY_GOVERNANCE.md` |
| **Run Artifact Contract** | Artifact schema | `docs/pm/RUN_ARTIFACT_CONTRACT.md` |
| **Master Architecture** | Technical Blueprint | `docs/agent/CODEMONKEYS_MASTER_ARCHITECTURE.md` |
| **Agent Boot Prompt** | Quick restore | `docs/pm/99_AGENT_BOOT_PROMPT.md` |
| **Decisions Log** | Major decisions | `docs/pm/DECISIONS.md` |

## 4. Current Status
- **Phase**: Bootstrap / Foundation (mostly complete).
- **What's Real**:
    - Dash MVP (fleet view, evidence, Nexus queue)
    - Formal schemas + report generator
    - Silverback validator (specs + artifacts + Nexus)
    - CI enforcement (on dev/main PRs)
    - Nexus inbox/outbox + executor
    - Branching workflow (main → dev ← feature/*)

## 5. Operating Protocol
1. **Branch**: `git checkout dev && git checkout -b feature/<name>`
2. **Spec**: Create/update spec using template
3. **Build**: Implement + tests
4. **Verify**: `./scripts/preflight.sh` or Silverback
5. **PR**: `feature/*` → `dev` (CI must pass)
6. **Release**: `dev` → `main` when ready

## 6. Next Milestones
- Merge pending feature branches to `dev`
- PR `dev` → `main` and tag `v0.2.0`
- Expand Science Monkeys integration (future)

## 7. Glossary
- **Silverback**: Governance enforcement agent.
- **Nexus**: Executive decision-maker (inbox/outbox/executor).
- **Banana Economy**: Resource budgeting system (time, tokens, runs).
- **Evidence Pack**: Proof of correctness (logs, schemas, CI results).
