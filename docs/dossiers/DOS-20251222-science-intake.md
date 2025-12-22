---
schema_version: "0.1"
dossier_id: "DOS-20251222-science-intake"
product_id: "codemonkeys-science"
owner: "nexus"
status: "approved"
created_at: "2025-12-22"
hypothesis:
  problem: "Science Monkeys produce research hypotheses/experiments, but there is no governed lane to convert them into actionable Code Monkeys work."
  claim: "A Science Dossier schema + intake commands enables bounded, traceable handoff from research to implementation."
  falsification: "If science dossiers cannot produce valid design dossiers, or if Oracle cannot plan against them."
mvp_boundary:
  in_scope:
    - "Science Dossier schema with hypothesis, acceptance hooks, evidence plan"
    - "codemonkeys dossier new-science / validate-science / science-to-design commands"
    - "Oracle planner recognizes science dossiers and emits conversion work orders"
  non_goals:
    - "LLM-based hypothesis generation"
    - "Automated experiment execution"
    - "Multi-step research pipelines"
acceptance_proofs:
  - "Proof 1: science dossier passes schema validation"
  - "Proof 2: science-to-design produces valid design dossier + spec scaffold"
  - "Proof 3: Oracle plans create_design_dossier work order from science dossier"
evidence:
  links: []
constitution_refs:
  - "constitution.md"
  - "docs/pm/00_VISION_STRATEGY.md"
  - "docs/pm/ROADMAP.md"
---

# Design Dossier: Science Intake (Sprint 6)

## 1. Context & Problem

Science Monkeys produce research:
- Hypotheses about ML/HPO techniques
- Experiment designs and results
- Acceptance criteria for "this works"

But there's no governed lane to:
- Convert a validated hypothesis into a product line
- Track lineage from research → design → spec → code
- Let Oracle plan the conversion steps

**Bottleneck:** Science output is lost in chat or ad-hoc docs instead of being fed into the factory.

## 2. Hypothesis

If we build a Science Dossier schema and intake commands, then:
- Science output becomes actionable factory input
- Conversion is bounded and traceable
- Oracle can plan the handoff automatically

**We know we're wrong if:**
- Science dossiers can't produce valid design dossiers
- The conversion loses critical information (hypothesis, proofs)
- Oracle can't plan work orders from science dossiers

## 3. MVP Definition

### In Scope
- **Science Dossier Schema**: hypothesis, experiment_links, acceptance_hooks, risks, evidence_plan
- **CLI commands**: new-science, validate-science, science-to-design
- **Oracle intents**: create_design_dossier, create_spec_from_dossier
- **One concrete example**: Convert an actual research topic

### Out of Scope
- LLM-driven science dossier authoring
- Automated experiment running
- Multi-hop research chains
- Dash "science lane" panel (defer to Sprint 7)

## 4. Evidence Plan

| Artifact | Description |
|----------|-------------|
| `docs/schemas/science_dossier.schema.json` | Schema definition |
| `docs/pm/SCIENCE_DOSSIER_TEMPLATE.md` | Human-editable template |
| `tests/dossiers/test_science_dossier.py` | Schema + conversion tests |
| Example science dossier | Concrete input for testing |
