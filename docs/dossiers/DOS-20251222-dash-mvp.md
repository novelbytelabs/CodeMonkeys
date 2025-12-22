---
schema_version: "0.1"
dossier_id: "DOS-20251222-dash-mvp"
product_id: "codemonkeys-dash"
owner: "nexus"
status: "approved"
created_at: "2025-12-22"
hypothesis:
  problem: "Operators cannot quickly see which products are real/compliant without manually hunting artifacts."
  claim: "A filesystem-backed Dash MVP makes fleet status and evidence discoverable in <1 minute."
  falsification: "If Dash can't render products/runs reliably from artifacts or fails silently on malformed data."
mvp_boundary:
  in_scope:
    - "Render products from dash/products.json"
    - "Render last run status from dash/runs/<product_id>/last_run.json"
    - "Explicit error states for missing/invalid artifacts"
  non_goals:
    - "Auth, multi-user, realtime updates, DB"
acceptance_proofs:
  - "pytest schema tests for products.json and last_run.json"
  - "Bootstrap proof artifact (screenshot or run evidence) stored under dash/runs/"
evidence:
  links: []
constitution_refs:
  - "constitution.md"
---

# Design Dossier: Dash MVP (v0.1)
Bootstrap dashboard to make fleet status and evidence visible from real artifacts.
