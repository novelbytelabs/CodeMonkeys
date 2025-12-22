# Spec: Design Dossier Intake

Dossier: DOS-20251221-dossier-intake
Constitution: constitution.md
Status: Draft
Owner: Nexus
Epic: Design Dossier Intake (Sprint 2)

## 1. Intent
Implement Design Dossier intake pipeline.

## 2. User Stories
User wants governance.

## 3. Functional Requirements
1. **Create Dossier Skeleton**: `codemonkeys dossier new <product_id>` creates `docs/dossiers/DOS-<date>-<slug>.md` with required frontmatter.
2. **Validate Dossier**: `codemonkeys dossier validate <path>` fails if required frontmatter keys are missing or `constitution_refs` is empty.
3. **Generate Spec From Dossier**: `codemonkeys dossier to-spec <dossier_path> --spec-id 002` creates/updates spec with `Dossier:` pointer.
4. **No-BS Evidence**: Pipeline must not claim validation passed unless filesystem artifacts exist and schema checks pass.

## 4. Acceptance Criteria
- **AC-001**: `codemonkeys dossier new` produces a dossier file with required frontmatter fields.
- **AC-002**: `codemonkeys dossier validate` fails when `constitution_refs` is missing/empty, passes when present and valid.
- **AC-003**: `codemonkeys dossier to-spec` produces a spec that includes a `Dossier:` reference and traceability map.
- **AC-004**: `pytest` includes coverage that enforces the above behaviors.

## 5. Owner & Authority
- Feature Owner: Nexus
- Governance: Inherits from Dossier DOS-20251221-dossier-intake.
- Approval: Human Operator.

## 6. Budget & Stop Conditions
- Budget: Standard.
- Stop Condition: Kill switch.

## 7. Constraints & Non-goals
### Constraints
- **C-001**: Local filesystem only; no external services required.
- **C-002**: Deterministic output paths under `docs/dossiers/` and `specs/`.
- **C-003**: Validation must be strict (fail fast, explicit messages).

### Non-goals
- **NG-001**: Auto-writing full specs beyond a scaffold.
- **NG-002**: Automated approvals or workflow orchestration.
- **NG-003**: LLM-based dossier/spec generation.

## 8. Evidence Plan
- Artifacts: Standard run artifacts.

## 9. Traceability Map
- `docs/dossiers/DOS-20251221-dossier-intake.md` -> `specs/002-dossier-intake/spec.md`
