# Spec: Design Dossier Intake

Dossier: DOS-20251221-dossier-intake
Status: Draft
Owner: Nexus
**Epic**: Design Dossier Intake (Sprint 2)

## 1. Intent
Make the Design Dossier the canonical upstream source for all manufacturing. Specs should not appear "from thin air"; they must be derived from a Dossier that justifies the investment. This feature implements the intake, validation, and conversion of Dossiers into Specs.

## 2. User Stories
- **As a Human**, I want to write a rationale-focused Dossier instead of a technical Spec first.
- **As Nexus**, I want to reject Dossiers that lack "Acceptance Proofs" so we don't build unverified junk.
- **As a Code Monkey**, I want to auto-generate a Spec skeleton from a Dossier to save typing.

## 3. Functional Requirements
1.  **Format**: Markdown with YAML front-matter (validated against JSON schema).
    - Location: `docs/dossiers/DOS-###-<slug>.md`
    - Schema: `docs/schemas/design_dossier.schema.json`
2.  **CLI**:
    - `codemonkeys dossier validate <path>`: Validates YAML front-matter + Markdown sections.
    - `codemonkeys dossier new <product_id>`: Generates file from template.
    - `codemonkeys dossier to-spec <path> [--spec-id ID]`: Generates Spec scaffold.
3.  **Escalation**:
    - If validation fails on proofs/fields -> Create Nexus Request.
    - Type: `clarification_required`.
4.  **Silverback Gate**:
    - Specs *must* reference a valid Dossier ID in headers.

## 4. Acceptance Criteria
1.  `codemonkeys dossier new banana` creates `docs/dossiers/DOS-###-banana.md` with YAML header.
2.  `codemonkeys dossier validate` passes for valid YAML+Markdown files.
3.  `codemonkeys dossier to-spec` creates `specs/XXX/spec.md` containing `Dossier: DOS-###` header.
4.  Deleting `acceptance_proofs` from a dossier triggers a `clarification_required` Nexus request.
5.  Silverback fails if a Spec exists without a valid Dossier reference.

## 5. Owner & Authority
- **Feature Owner**: Nexus Agent
- **Governance**: Dossier > Spec.
- **Approval**: Human governance required for Dossier structure changes.

## 6. Budget & Stop Conditions
- **Budget**: N/A (CLI operation).
- **Stop Condition**: Kill switch enabled.

## 7. Constraints & Non-goals
- **Constraint**: Must use `python-frontmatter` or regex for parsing to avoid heavy deps.
- **Constraint**: Nexus schema must be updated to support `clarification_required`.
- **Non-goal**: Automatic code generation from Dossier.

## 8. Evidence Plan
- **Artifacts**: Dossier files, Generated Specs, Nexus Requests.
- **Logs**: validation logs.

## 9. Traceability Map
- `docs/schemas/design_dossier.schema.json` -> `src/codemonkeys/commands/dossier.py`

