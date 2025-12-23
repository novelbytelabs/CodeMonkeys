---
schema_version: "0.1"
dossier_id: "DOS-20251222-multi-product-portfolio-governance"
product_id: "codemonkeys-portfolio"
owner: "nexus"
status: "approved"
created_at: "2025-12-22"
hypothesis:
  problem: "Factory can only cleanly operate single product. Multi-product governance, per-product isolation, and repo cutover readiness are missing."
  claim: "Hardening product registry, Oracle per-product scoping, and cutover rehearsal enables multi-product portfolio governance."
  falsification: "If Oracle cannot plan across 3+ products or cutover rehearsal fails."
mvp_boundary:
  in_scope:
    - "Product registry with repo_root, owner, criticality, sla_tier"
    - "Oracle per-product execution roots"
    - "Cutover rehearsal script and dossier"
    - "CI portfolio health check"
  non_goals:
    - "Actual repo migration"
    - "Cross-repo Oracle execution"
    - "Product creation automation"
acceptance_proofs:
  - "Proof 1: products.json schema validates 3+ products"
  - "Proof 2: oracle plan --from-schedules works across multiple products"
  - "Proof 3: cutover rehearsal exports working subset"
  - "Proof 4: CI dry-run portfolio validation passes"
evidence:
  links: []
constitution_refs:
  - "constitution.md"
  - "docs/pm/ROADMAP.md"
---

# Design Dossier: Multi-Product Portfolio Governance (Sprint 8)

## 1. Context & Problem

With v0.7.1, the factory has:
- Schedule-based planning
- gc_runs and drift_check intents
- Science Lane visibility

But it lacks:
- Multi-product governance (3+ products with distinct schedules)
- Per-product execution isolation
- Repo cutover readiness

## 2. Hypothesis

If we harden the product registry, add per-product Oracle scoping, and implement cutover rehearsal, then:
- Fleet ops work across multiple products
- Each product has isolated artifacts and runs
- Migration to new repo structure is rehearsed and safe

## 3. MVP Definition

### In Scope
1. **Product Registry Hardening**: repo_root, owner, criticality, sla_tier
2. **Oracle Per-Product Roots**: executor scopes to product paths
3. **Cutover Rehearsal**: script to export/validate subset
4. **CI Readiness**: dry-run portfolio validation

### Non-goals
- Actual repo migration (Sprint 9+)
- Cross-repo Oracle execution
- Product creation automation

## 4. Evidence Plan

| Artifact | Purpose |
|----------|---------|
| `dash/schemas/products.schema.json` | Product registry schema |
| `scripts/cutover_rehearsal.py` | Export validator |
| `tests/portfolio/test_products_schema.py` | Schema tests |
| `tests/portfolio/test_cutover.py` | Cutover tests |
