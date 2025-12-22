# Spec: Science Intake

Dossier: DOS-20251222-science-intake
Constitution: constitution.md
Status: Draft
Owner: nexus
Epic: Science Intake (Sprint 6)

## 1. Intent
Science Monkeys produce research hypotheses/experiments, but there is no governed lane to convert them into actionable Code Monkeys work.
A Science Dossier schema + intake commands enables bounded, traceable handoff from research to implementation.

## 2. User Stories
- **As a Science Monkey**, I want to create a science dossier that captures my hypothesis and acceptance hooks so Code Monkeys can implement it.
- **As Nexus**, I want to validate science dossiers against a schema so only well-formed research enters the factory.
- **As Nexus**, I want to convert a science dossier to a design dossier + spec scaffold automatically.
- **As an Operator**, I want Oracle to plan work orders from science dossiers so the handoff is bounded and traceable.

## 3. Functional Requirements
- **FR-001**: Science Dossier schema in `docs/schemas/science_dossier.schema.json` with required fields: hypothesis, acceptance_hooks, evidence_plan, constitution_refs.
- **FR-002**: `codemonkeys dossier new-science <topic>` creates a science dossier template.
- **FR-003**: `codemonkeys dossier validate-science <path>` validates against schema.
- **FR-004**: `codemonkeys dossier science-to-design <path>` produces design dossier + spec scaffold with traceability.
- **FR-005**: Oracle planner recognizes science dossiers and emits `create_design_dossier` work orders.

## 4. Acceptance Criteria
- **AC-001**: Science dossier passes schema validation.
- **AC-002**: `science-to-design` produces valid design dossier + spec scaffold.
- **AC-003**: Oracle plans `create_design_dossier` work order from science dossier.
- **AC-004**: Traceability map links science → design → spec.

## 5. Owner & Authority
- **Feature Owner**: nexus
- **Governance**: Inherits from Dossier DOS-20251222-science-intake.
- **Approval**: Human Operator.

## 6. Budget & Stop Conditions
- **Budget**: Max 3 work orders per science dossier conversion.
- **Stop Condition**: Kill switch, schema validation failure, missing constitution refs.

## 7. Constraints & Non-goals
### Constraints
- **C-001**: Science dossiers must reference at least one constitution document.
- **C-002**: Conversion must preserve hypothesis and acceptance hooks in the design dossier.
- **C-003**: Traceability must be explicit and machine-readable.

### Non-goals
- **NG-001**: LLM-based hypothesis generation.
- **NG-002**: Automated experiment execution.
- **NG-003**: Multi-step research pipelines.

## 8. Evidence Plan
- **Artifacts**: `docs/schemas/science_dossier.schema.json`, `tests/dossiers/test_science_dossier.py`
- **Example**: `docs/dossiers/SCI-20251222-arqonhpo-runtime-optimization.md`

## 9. Traceability Map
| Source | Target | Relation |
|--------|--------|----------|
| `DOS-20251222-science-intake.md` | `specs/006-science-intake/spec.md` | dossier → spec |
| `SCI-20251222-arqonhpo-runtime-optimization.md` | (pending design dossier) | science → design |
