# Docs Map and Integration Notes

Date: 2025-12-21
Status: Draft

Goal: keep a stable doc hierarchy so we can restart ChatGPT sessions without losing context.

## Canonical doc sources (authoritative)
- `constitution.md` → will be distilled into **Code Monkeys Constitution** (single source)
- `VISION.md` → product vision and north star
- `CODEMONKEYS_MASTER_ARCHITECTURE.md` → canonical architecture (top-level)
- `CODEMONKEYS_ARCHITECTURE_v2.md` → refined v0.1 architecture after critique (**must be merged into Master**)
- `ORCHESTRATOR_ARCHITECTURE.md` → Ship orchestrator design (Admiral/Marines, DB-backed campaigns)
- `RULE_SCHEMA_SPEC.md` → Living Linter rule schema
- `SHIP_INTEGRATION_PLAN.md` → integration tasks with external tools

## Merge guidance: ARCHITECTURE_v2 → MASTER_ARCHITECTURE
Treat `CODEMONKEYS_ARCHITECTURE_v2.md` as the newest "decision record" for:
- reduced agent set (3 core agents)
- banana economy cost model update
- governance.lock format
- chaos monkey split (fuzz vs fault)

Action:
1) Update `CODEMONKEYS_MASTER_ARCHITECTURE.md` to include the v2 choices as the canonical design.
2) Keep ARCHITECTURE_v2 as an appendix/changelog: "post-critique deltas" only.

## “Context Pack” for future sessions
Maintain a small, always-current snapshot file:
- `CONTEXT_SNAPSHOT.md` (1–2 pages)
Contains:
- system contract summary
- current naming (Code Monkeys Dash, Nexus, Science/Code swarms)
- current architecture decisions
- current backlog

This file is what you paste into a fresh ChatGPT session to restore context quickly.
