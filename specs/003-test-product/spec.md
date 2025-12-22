# Spec: test-product

Dossier: DOS-20251222-test-product
Constitution: constitution.md
Status: Draft
Owner: nexus
Epic: test-product

## 1. Intent
We need to test governance.
This will pass verification.

## 2. User Stories
- **As a Developer**, I want a test product entry to validate the governance pipeline without requiring a real product.
- **As an Operator**, I want to verify that Dash renders test products correctly before adding production products.

## 3. Functional Requirements
- **FR-001**: Provide a minimal product entry in `dash/products.json` for demonstration/testing.
- **FR-002**: Maintain a `dash/runs/test-product/last_run.json` that conforms to schema.
- **FR-003**: Include at least one evidence artifact referenced by last_run.json.

## 4. Acceptance Criteria
1. Proof 1: Valid proof

## 5. Owner & Authority
- **Feature Owner**: nexus
- **Governance**: Inherits from Dossier DOS-20251222-test-product.
- **Approval**: Human Operator.

## 6. Budget & Stop Conditions
- **Budget**: Standard.
- **Stop Condition**: Kill switch.

## 7. Constraints & Non-goals
### Constraints
- **C-001**: Must remain deterministic and self-contained (no network calls).
- **C-002**: Must generate valid "happy path" artifacts for pipeline verification.

### Non-goals
- **NG-001**: No production shipping or release tagging.
- **NG-002**: No integration with external services or secret material.

## 8. Evidence Plan
- **Artifacts**: Standard run artifacts.

## 9. Traceability Map
- `docs/dossiers/DOS-20251222-test-product.md` -> `specs/003-test-product/spec.md`
