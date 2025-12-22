---
schema_version: "0.1"
dossier_id: "DOS-20251222-factory-cli"
product_id: "codemonkeys-cli"
owner: "nexus"
status: "approved"
created_at: "2025-12-22"
hypothesis:
  problem: "Ad-hoc scripts and inconsistent invocation allow bypassing governance and make runs non-repeatable."
  claim: "A single codemonkeys CLI standardizes execution, validation, and shipping under one governed interface."
  falsification: "If operators can still ship without Silverback passing or without evidence artifacts."
mvp_boundary:
  in_scope:
    - "codemonkeys run / dash / silverback / nexus / ship entry points"
    - "Consistent exit codes and artifact paths"
  non_goals:
    - "LLM authoring, remote orchestration, multi-node execution"
acceptance_proofs:
  - "pytest gate tests for ship preflight"
  - "Silverback passes for all registered products"
evidence:
  links: []
constitution_refs:
  - "constitution.md"
---

# Design Dossier: Factory CLI
Single governed CLI interface to run, validate, and ship.
