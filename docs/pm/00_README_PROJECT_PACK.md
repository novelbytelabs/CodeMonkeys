# Code Monkeys — Project Pack (for Antigravity AI)

Date: 2025-12-21

This pack is a **context snapshot** for the Code Monkeys program.
It is meant to be pasted/loaded into Antigravity AI so it can act as the repo manager / implementer,
while ChatGPT (me) acts as **Project Manager**.

## What we are building
A **solo-run software production factory** that can create and maintain a large portfolio of products from one workstation.

There are *two* autonomous swarms:

1) **Science Monkeys** — R&D / invention loop:
   Explore → Hypothesize → Design → Execute → Interpret → Share.
   Output: research artifacts, proofs, experiment results, product concepts, product line proposals.

2) **Code Monkeys** — production/maintenance loop:
   Receives Science outputs at the Design stage and turns them into production software:
   specs, tests, code, docs, CI, releases, maintenance, and fleet rollouts.

A top-level organizational agent, **Nexus Agent**, acts as Product Owner / Executive:
- Makes most decisions in the human's absence
- Learns human preferences
- Routes work across products
- Enforces governance via the Constitution

You (the human) supervise via **Code Monkeys Dash** (formerly "Code Monkeys Org").

## Immediate goal
Define the **operating contract** for Human ↔ Nexus ↔ Swarms, and determine whether:
- **Constitution + Spec** are sufficient authoritative inputs for autonomous execution, or
- we need an additional authoritative artifact (e.g., Design Dossier / Proof Bundle) for Science→Code handoff.

## Key repo docs to integrate
- CODEMONKEYS_ARCHITECTURE_v2.md (post-critique refined architecture)
- ORCHESTRATOR_ARCHITECTURE.md (Ship orchestrator)
- RULE_SCHEMA_SPEC.md (Living Linter rule schema)
- SHIP_INTEGRATION_PLAN.md (external tool integration plan)
- constitution.md (legacy Code Monkeys constitution; to be distilled into a single Code Monkeys Constitution)

## Near-term deliverables (PM-defined)
1) SYSTEM_CONTRACT.md (authority & responsibility split; gates; kill switch)
2) HANDOFF_CONTRACT.md (Science→Code Design Dossier schema)
3) SPEC_TEMPLATE_AUDIT.md (is spec-template sufficient? what must change)
4) DOCS_MAP.md (doc hierarchy + where architecture_v2 merges)
