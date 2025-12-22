---
schema_version: "0.1"
dossier_id: "DOS-20251222-release-gate"
product_id: "release-gate"
owner: "nexus"
status: "draft"
created_at: "2025-12-22"
hypothesis:
  problem: "Code can currently be released without verification, violating Article I of the Constitution."
  claim: "Implementing a strict Release Gate will prevent non-compliant code from leaving the Factory."
  falsification: "If we can tag/release code without an Evidence Pack."
mvp_boundary:
  in_scope:
    - "CLI command 'codemonkeys ship' (release wrapper)"
    - "Pre-release verification check (Silverback spec)"
    - "Git tag blocking (optional hook or CLI logic)"
  non_goals:
    - "GitHub Actions pipeline (Sprint 5)"
acceptance_proofs:
  - "Proof 1: 'codemonkeys ship' fails if no artifacts exist."
  - "Proof 2: 'codemonkeys ship' succeeds if verification passes."
evidence:
  links: []
constitution_refs:
  - "constitution.md"
  - "docs/pm/00_VISION_STRATEGY.md"
---

# Design Dossier: [Product Name]

## 1. Context & Problem
[Why are we doing this? Link to strategy]

## 2. Hypothesis
[If we build X, then Y will happen. We know we are wrong if Z.]

## 3. MVP Definition
[Strict boundary of what is IN and OUT]

## 4. Evidence Plan
[How will we prove it works? Specific artifacts]
