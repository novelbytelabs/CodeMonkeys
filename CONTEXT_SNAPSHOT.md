# CONTEXT SNAPSHOT: Code Monkeys
**Date:** 2025-12-21
**Version:** 0.1 (Bootstrap)

## 0. How to Resume (Start Here)
- **Last Checkpoint**: P4 complete (Hardened generator + gc_runs + validity badges).
- **Current Milestone**: P5 (Constitution implementation + governance enforcement).
- **Commit Hashes**:
    - P2: `2c8822f` (Bootstrap MVP)
    - P3: `371806e` (Schemas + report generator)
    - P4: `730fb7f` (Hardened generator + gc_runs)
- **Branch Status**: `000-dash-mvp` ready to merge to `main`.
- **Next 3 Tasks**:
    1. Merge to main + tag `v0.1.0-dash`.
    2. Create `AUTONOMY_GOVERNANCE.md` (enforceable rules).
    3. Add Silverback validator + preflight scripts.
- **Open Decisions**:
    - [Decision]: How strict to make Silverback in bootstrap (fail vs warn).
    - [Decision]: Which sections are truly mandatory vs recommended.
- **Canonical 'Start Here' Files**:
    - `CONTEXT_SNAPSHOT.md` (This file)
    - `docs/pm/01_SYSTEM_CONTRACT.md` (Roles)
    - `docs/pm/RUN_ARTIFACT_CONTRACT.md` (Artifact contract)
    - `specs/000-dash-mvp/spec.md` (Dash MVP spec)

## 1. Overview
Code Monkeys is an autonomous software production factory for a solo operator. It consists of two swarms:
- **Science Monkeys** (R&D): Discover and design products.
- **Code Monkeys** (Production): Build, ship, and maintain products.
- **Nexus Agent**: Organizational Product Owner (Executive decision-maker).

The system is "governance-first," prioritizing clear rules, evidence-based claims, and bounded autonomy.

## 2. Authority Model
1.  **Constitution**: The highest authority. Non-negotiable rules for all agents and users.
2.  **Human (User)**: Portfolio supervisor. Governance designer.
3.  **Nexus Agent**: Product Owner. Makes autonomous decisions within Constitutional bounds.
4.  **Swarms**: Execution engines. Bound by Spec and Constitution.

## 3. Canonical Documentation
| Doc | Purpose | Location |
|---|---|---|
| **System Contract** | Roles & Responsibilities | `docs/pm/01_SYSTEM_CONTRACT.md` |
| **Master Architecture** | Technical Blueprint | `docs/agent/CODEMONKEYS_MASTER_ARCHITECTURE.md` |
| **Handoff Contract** | Science → Code Protocol | `docs/pm/02_HANDOFF_CONTRACT.md` |
| **Constitution** | Governance Rules | `constitution.md` (root) |
| **Spec Template** | Feature Requirements | `.specify/templates/spec-template.md` |

*(Note: Architecture v2 has been integrated into Master as Appendix A)*

## 4. Current Status
- **Phase**: Bootstrap / Foundation.
- **Active Tasks**:
    - Integrating governance docs.
    - Refining spec templates for autonomy.
    - Establishing the "Banana Economy" (resource budgeting).

## 5. Operating Protocol
1.  **Plan**: create `implementation_plan.md` (requires approval).
2.  **Spec**: `codemonkeys dev spec` (using template).
3.  **Build**: Code Monkey executes plan.
4.  **Verify**: Chaos Monkey & Silverback enforce quality.
5.  **Ship**: Evidence Pack required for release.

## 6. Next Milestones
- **v0.1**: Foundation (CLI, Governance, Basic Implementer).
- **v0.2**: Dev Loop (Spec/Plan/Tasks, Chaos Monkey, Scout).
- **v0.3**: Ship Pillars (Docs, CI, PR).

## 7. Glossary
- **Silverback**: Governance enforcement agent.
- **Code Monkey**: Builder agent.
- **Foreman**: Planner agent.
- **Banana Economy**: Resource budgeting system (time, tokens, runs).
- **Design Dossier**: Required artifact for Science → Code handoff.
- **Evidence Pack**: Proof of correctness (logs, screenshots, CI results).
