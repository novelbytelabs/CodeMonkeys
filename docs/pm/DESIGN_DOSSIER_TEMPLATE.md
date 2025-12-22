---
schema_version: "0.1"
dossier_id: "DOS-[YYYYMMDD-ID]"
product_id: "[product-slug]"
owner: "nexus"
status: "draft"
created_at: "[YYYY-MM-DD]"
hypothesis:
  problem: "[One sentence problem statement]"
  claim: "[One sentence hypothesis]"
  falsification: "[What makes this false?]"
mvp_boundary:
  in_scope:
    - "[Feature 1]"
    - "[Feature 2]"
  non_goals:
    - "[Out of scope item]"
acceptance_proofs:
  - "[Proof 1: e.g. CLI command returns 0]"
  - "[Proof 2: e.g. Artifact X exists]"
evidence:
  links: []
constitution_refs:
  - "constitution.md"
  - "docs/pm/00_VISION_STRATEGY.md"
---

# Design Dossier: [Feature Name]

## 1. Context & Rationale
[Expand on the YAML hypothesis here. Why is this important? alignment with strategy?]

## 2. Experiments
**Experiment 1**: [Description]
- **Goal**: [What do we want to learn?]
- **Result**: [To be filled after experiment]

## 3. Implementation Request
**To Code Monkeys**: Manufacture a Spec based on this dossier.
