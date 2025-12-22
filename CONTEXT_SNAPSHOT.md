# CONTEXT SNAPSHOT: Code Monkeys
**Date:** 2025-12-21
**Version:** 0.3 (Foundation Complete)

## 0. How to Resume (Start Here)
- **Last Checkpoint**: Release v0.2.1 (Spec Kit fixed).
- **Current Milestone**: Sprint 1: Factory Core CLI.
- **Commit Hashes (main)**: `e0d2db0` (v0.2.0), `v0.2.1` (Spec Kit fix)
- **Branch Status**:
    - `main`: Stable v0.2.1
    - `dev`: Synced
    - `feature/factory-cli`: **Pending Creation**
- **Canonical 'Start Here' Files**:
    - `docs/pm/00_VISION_STRATEGY.md` (North Star)
    - `docs/pm/ROADMAP.md` (Phases)
    - `docs/pm/MASTER_BACKLOG.md` (Epics)
    - `docs/pm/99_AGENT_BOOT_PROMPT.md` (Quick Restore)

## 1. Overview
Code Monkeys is an autonomous software production factory.
- **Vision**: Repeatable manufacturing loop (Spec -> Artifacts).
- **Control**: Nexus (Executive) + Silverback (Sheriff) + CLI (Spine).
- **State**: 5 Products, fully governed, CI enforced.

## 2. Current Sprint: Phase 1 (Factory Core CLI)
**Goal**: Unified `codemonkeys` CLI to replace ad-hoc scripts.
**Deliverables**:
- `codemonkeys dash serve`
- `codemonkeys run <product>`
- `codemonkeys silverback`
- `codemonkeys nexus exec`

## 3. Canonical Documentation
| Doc | Purpose | Location |
|---|---|---|
| **Vision** | Strategy/Pillars | `docs/pm/00_VISION_STRATEGY.md` |
| **Roadmap** | Phases/Sprints | `docs/pm/ROADMAP.md` |
| **Backlog** | Epics/Acceptance | `docs/pm/MASTER_BACKLOG.md` |
| **Governance** | Rules/Constitutional | `docs/pm/AUTONOMY_GOVERNANCE.md` |
| **Decisions** | Strategic Log | `docs/pm/DECISIONS.md` |

## 4. Operational Protocols
- **Branch**: `feature/*` -> `dev` -> `main`
- **Verification**: `silverback --all` + `pytest` + CI
- **Governance**: No changes without formatted Spec + Plan
- **Evidence**: All claims must have artifacts
