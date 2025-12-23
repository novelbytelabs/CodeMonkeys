# Spec: Multi-Product Portfolio Governance (Sprint 8)

Dossier: DOS-20251222-multi-product-portfolio-governance
Constitution: constitution.md
Status: Draft
Owner: nexus
Epic: Multi-Product Portfolio

## 1. Intent
Factory can only cleanly operate single product. Multi-product governance, per-product isolation, and repo cutover readiness are missing.
Hardening product registry, Oracle per-product scoping, and cutover rehearsal enables multi-product portfolio governance.

## 2. User Stories
- **As an Operator**, I want to manage multiple products with distinct schedules so each has appropriate governance.
- **As Nexus**, I want per-product execution roots so artifacts are isolated.
- **As an Operator**, I want cutover rehearsal so I can validate migrations before executing.
- **As CI**, I want dry-run portfolio validation to ensure integrity.

## 3. Functional Requirements
- **FR-001**: Products schema includes criticality, sla_tier, schedule_path, enabled fields.
- **FR-002**: Products registry contains 3+ products with schedules.
- **FR-003**: `oracle plan --from-schedules` generates work orders across multiple products.
- **FR-004**: `scripts/cutover_rehearsal.py` exports canonical subset.
- **FR-005**: Exported subset passes pytest validation.

## 4. Acceptance Criteria
- **AC-001**: products.json schema validates 3+ products.
- **AC-002**: `oracle plan --from-schedules` works across multiple products (8+ work orders).
- **AC-003**: cutover rehearsal exports working subset.
- **AC-004**: CI dry-run portfolio validation passes.

## 5. Owner & Authority
- **Feature Owner**: nexus
- **Governance**: Inherits from Dossier DOS-20251222-multi-product-portfolio-governance.
- **Approval**: Human Operator.

## 6. Budget & Stop Conditions
- **Budget**: Max 10 work orders per scheduled run.
- **Stop Condition**: Kill switch, on_test_fail, on_silverback_fail.

## 7. Constraints & Non-goals
### Constraints
- **C-001**: Cutover rehearsal is read-only (no mutations to source).
- **C-002**: Multi-product planning respects per-product budgets.

### Non-goals
- **NG-001**: Actual repo migration (Sprint 9+).
- **NG-002**: Cross-repo Oracle execution.
- **NG-003**: Product creation automation.

## 8. Evidence Plan
- **Artifacts**: `dash/schemas/products.schema.json`, `dash/products.json`, schedules.
- **Tests**: `tests/portfolio/test_products_schema.py` (9 tests).

## 9. Traceability Map
| Source | Target | Relation |
|--------|--------|----------|
| `DOS-20251222-multi-product-portfolio-governance.md` | `specs/008-.../spec.md` | dossier → spec |
| `products.schema.json` | `products.json` | schema → instance |
