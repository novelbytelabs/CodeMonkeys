---
schema_version: "0.1"
dossier_id: "DOS-20251221-dossier-intake"
product_id: "dossier-intake"
owner: "nexus"
status: "approved"
created_at: "2025-12-21"
hypothesis:
  problem: "Specs are created ad-hoc without justification."
  claim: "Enforcing upstream dossiers will fix this."
  falsification: "If people bypass it."
mvp_boundary:
  in_scope:
    - "CLI commands"
    - "Schema"
  non_goals:
    - "Full LLM generation"
acceptance_proofs:
  - "Silverback validates dossier existence"
evidence:
  links: []
constitution_refs:
  - "constitution.md"
  - "docs/pm/00_VISION_STRATEGY.md"
---

# Design Dossier: Dossier Intake
Retroactive dossier for Sprint 2/3.
