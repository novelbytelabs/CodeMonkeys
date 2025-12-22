
import click
import frontmatter
import json
import re
from pathlib import Path
from datetime import datetime
from jsonschema import validate, ValidationError

@click.group()
def dossier():
    """Manage Design Dossiers."""
    pass

@dossier.command()
@click.argument('product_slug')
def new(product_slug):
    """Create a new Design Dossier from template."""
    template_path = Path("docs/pm/DESIGN_DOSSIER_TEMPLATE.md")
    if not template_path.exists():
        click.echo(f"Error: Template not found at {template_path}", err=True)
        exit(1)

    today = datetime.now().strftime("%Y%m%d")
    dossier_id = f"DOS-{today}-{product_slug}"
    filename = f"{dossier_id}.md"
    target_path = Path("docs/dossiers") / filename
    
    # Ensure directory exists
    target_path.parent.mkdir(parents=True, exist_ok=True)

    if target_path.exists():
        click.echo(f"Error: Dossier {filename} already exists", err=True)
        exit(1)

    content = template_path.read_text()
    
    # Replace placeholders
    content = content.replace("[product-slug]", product_slug)
    content = content.replace("[YYYYMMDD]", today)
    content = content.replace("[YYYY-MM-DD]", datetime.now().strftime("%Y-%m-%d"))
    # We leave other placeholders for the user to fill

    target_path.write_text(content)
    click.echo(f"Created Dossier: {target_path}")


@dossier.command()
@click.argument('dossier_path', type=click.Path(exists=True))
def validate_cmd(dossier_path):
    """Validate a Design Dossier against the schema."""
    path = Path(dossier_path)
    click.echo(f"Validating Dossier: {path}")

    # Load Schema
    schema_path = Path("docs/schemas/design_dossier.schema.json")
    if not schema_path.exists():
        click.echo("Error: Schema not found", err=True)
        exit(1)
    
    schema = json.loads(schema_path.read_text())

    # Load Dossier
    try:
        post = frontmatter.load(path)
    except Exception as e:
        click.echo(f"Error parsing frontmatter: {e}", err=True)
        _escalate_to_nexus(path, f"Frontmatter parse error: {e}")
        exit(1)

    # Validate Schema
    try:
        validate(instance=post.metadata, schema=schema)
        click.echo("YAML Schema Valid")
    except ValidationError as e:
        click.echo(f"Schema Error: {e.message}", err=True)
        _escalate_to_nexus(path, f"Schema validation error: {e.message}")
        exit(1)

    # Validate Content (Placeholders)
    content = post.content
    if "[One sentence problem statement]" in str(post.metadata) or "[Proof 1" in str(post.metadata):
         click.echo("Validation Failed: Placeholders detected in metadata", err=True)
         _escalate_to_nexus(path, "Placeholders detected in metadata")
         exit(1)
    
    click.echo("Dossier Valid")


@dossier.command("to-spec")
@click.argument('dossier_path', type=click.Path(exists=True))
@click.option('--spec-id', default=None, help="Manual spec ID (e.g. 005)")
def to_spec(dossier_path, spec_id):
    """Generate a Spec skeleton from a Dossier."""
    path = Path(dossier_path)
    post = frontmatter.load(path)
    meta = post.metadata
    
    product_slug = meta.get('product_id', 'unknown')
    
    # Determine Spec ID
    if not spec_id:
        existing_specs = list(Path("specs").glob("[0-9][0-9][0-9]-*"))
        if existing_specs:
            last_id = sorted([p.name[:3] for p in existing_specs])[-1]
            next_id = int(last_id) + 1
            spec_id = f"{next_id:03d}"
        else:
            spec_id = "001"
            
    spec_dir = Path(f"specs/{spec_id}-{product_slug}")
    spec_dir.mkdir(parents=True, exist_ok=True)
    spec_file = spec_dir / "spec.md"
    
    if spec_file.exists():
        click.echo(f"Error: Spec file already exists at {spec_file}", err=True)
        exit(1)
        
    # Spec Scaffold
    constitution_refs = meta.get('constitution_refs', ['constitution.md'])
    const_block = "\n".join([f"- {ref}" for ref in constitution_refs])

    content = f"""# Spec: {product_slug}

Dossier: {meta.get('dossier_id')}
Constitution: constitution.md
Status: Draft
Owner: {meta.get('owner')}
Epic: {product_slug}

## 1. Intent
{post.metadata.get('hypothesis', {}).get('problem', 'Problem statement...')}
{post.metadata.get('hypothesis', {}).get('claim', 'Hypothesis...')}

## 2. User Stories
- **As a User**, I want [feature] so that [benefit].

## 3. Functional Requirements
1.  **Requirement 1**: ...

## 4. Acceptance Criteria
"""
    for proof in meta.get('acceptance_proofs', []):
        content += f"1. {proof}\n"

    content += f"""
## 5. Owner & Authority
- **Feature Owner**: {meta.get('owner')}
- **Governance**: Inherits from Dossier {meta.get('dossier_id')}.
- **Approval**: Human Operator.

## 6. Budget & Stop Conditions
- **Budget**: Standard.
- **Stop Condition**: Kill switch.

## 7. Constraints & Non-goals
**Non-goals**:
"""
    for ng in meta.get('mvp_boundary', {}).get('non_goals', []):
        content += f"- {ng}\n"

    content += f"""
## 8. Evidence Plan
- **Artifacts**: Standard run artifacts.

## 9. Traceability Map
- `docs/dossiers/{path.name}` -> `specs/{spec_id}-{product_slug}/spec.md`
"""
    
    spec_file.write_text(content)
    click.echo(f"Generated Spec: {spec_file}")


def _escalate_to_nexus(dossier_path, reason):
    """Create a Nexus request for clarification."""
    click.echo("Validation Failed")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    req_file = Path(f"nexus/inbox/req_{timestamp}_dossier_escalation.json")
    
    payload = {
        "schema_version": "0.1",
        "request_id": f"req_{timestamp}",
        "type": "clarification_required",
        "source": "silverback_cli",
        "created_at": datetime.now().isoformat(),
        "status": "pending",
        "priority": "high",
        "payload": {
             "description": f"Dossier validation failed for {dossier_path}: {reason}",
             "context": str(dossier_path)
        }
    }
    
    req_file.write_text(json.dumps(payload, indent=2))
    click.echo(f"Nexus escalation created: \n{req_file}")


# ============================================================================
# Science Dossier Commands
# ============================================================================

SCIENCE_DOSSIER_TEMPLATE = '''---
schema_version: "0.1"
dossier_type: "science"
dossier_id: "SCI-{date}-{slug}"
topic: "{topic}"
owner: "science-monkeys"
status: "draft"
created_at: "{date_iso}"
hypothesis:
  statement: "[Main hypothesis - what you believe will happen if you do X]"
  null_hypothesis: "[What would disprove the hypothesis]"
  significance_level: 0.05
experiment_links:
  - name: "[Experiment or codebase name]"
    path: "[Path or URL to experiment]"
    description: "[Brief description]"
acceptance_hooks:
  code_proofs:
    - "[Proof 1: e.g., benchmark shows < Xms latency]"
    - "[Proof 2: e.g., test passes on edge cases]"
  test_requirements:
    - "[Test requirement 1]"
  evidence_artifacts:
    - "[Expected artifact path]"
risks:
  - risk: "[Risk description]"
    mitigation: "[How to mitigate]"
constraints:
  - "[Constraint 1]"
evidence_plan:
  final_artifacts:
    - "[Final artifact 1]"
  validation_method: "[How to validate]"
constitution_refs:
  - "constitution.md"
---

# Science Dossier: {topic}

## 1. Research Question

[What question does this research answer?]

## 2. Hypothesis

> [Your hypothesis statement]

**Falsification criteria:**
- [What would prove this wrong]

## 3. Key Innovations

[What's new/different about this approach]

## 4. Current Evidence

| Proof | Status | Evidence |
|-------|--------|----------|
| [Proof 1] | [Status] | [Evidence] |

## 5. Handoff Requirements

For Code Monkeys to productize this:
1. [Requirement 1]
'''


@dossier.command("new-science")
@click.argument('topic_slug')
def new_science(topic_slug):
    """Create a new Science Dossier from template."""
    today = datetime.now().strftime("%Y%m%d")
    date_iso = datetime.now().strftime("%Y-%m-%d")
    dossier_id = f"SCI-{today}-{topic_slug}"
    filename = f"{dossier_id}.md"
    target_path = Path("docs/science") / filename
    
    # Ensure directory exists
    target_path.parent.mkdir(parents=True, exist_ok=True)

    if target_path.exists():
        click.echo(f"Error: Science dossier {filename} already exists", err=True)
        exit(1)

    # Format topic name
    topic = topic_slug.replace("-", " ").title()
    
    content = SCIENCE_DOSSIER_TEMPLATE.format(
        date=today,
        date_iso=date_iso,
        slug=topic_slug,
        topic=topic
    )

    target_path.write_text(content)
    click.echo(f"Created Science Dossier: {target_path}")


@dossier.command("validate-science")
@click.argument('dossier_path', type=click.Path(exists=True))
def validate_science(dossier_path):
    """Validate a Science Dossier against the schema."""
    path = Path(dossier_path)
    click.echo(f"Validating Science Dossier: {path}")

    # Load Schema
    schema_path = Path("docs/schemas/science_dossier.schema.json")
    if not schema_path.exists():
        click.echo("Error: Science dossier schema not found", err=True)
        exit(1)
    
    schema = json.loads(schema_path.read_text())

    # Load Dossier
    try:
        post = frontmatter.load(path)
    except Exception as e:
        click.echo(f"Error parsing frontmatter: {e}", err=True)
        exit(1)

    # Check dossier_type
    if post.metadata.get('dossier_type') != 'science':
        click.echo("Error: dossier_type must be 'science'", err=True)
        exit(1)

    # Validate Schema
    try:
        validate(instance=post.metadata, schema=schema)
        click.echo("Schema Valid")
    except ValidationError as e:
        click.echo(f"Schema Error: {e.message}", err=True)
        exit(1)

    # Check constitution refs exist
    constitution_refs = post.metadata.get('constitution_refs', [])
    for ref in constitution_refs:
        ref_path = Path(ref)
        # Check in repo root and common locations
        if not ref_path.exists() and not Path(f".agent/{ref}").exists():
            click.echo(f"Warning: constitution_ref '{ref}' not found locally")
    
    click.echo("Science Dossier Valid")


@dossier.command("science-to-design")
@click.argument('science_path', type=click.Path(exists=True))
@click.option('--product-id', required=True, help="Product ID for the design dossier")
def science_to_design(science_path, product_id):
    """Convert a Science Dossier to a Design Dossier scaffold."""
    path = Path(science_path)
    
    # Load science dossier
    try:
        post = frontmatter.load(path)
    except Exception as e:
        click.echo(f"Error parsing science dossier: {e}", err=True)
        exit(1)
    
    meta = post.metadata
    
    # Validate it's a science dossier
    if meta.get('dossier_type') != 'science':
        click.echo("Error: Input must be a science dossier (dossier_type: science)", err=True)
        exit(1)
    
    today = datetime.now().strftime("%Y%m%d")
    date_iso = datetime.now().strftime("%Y-%m-%d")
    design_id = f"DOS-{today}-{product_id}"
    design_file = Path(f"docs/dossiers/{design_id}.md")
    
    if design_file.exists():
        click.echo(f"Error: Design dossier {design_file} already exists", err=True)
        exit(1)
    
    # Build acceptance proofs from science hooks
    acceptance_hooks = meta.get('acceptance_hooks', {})
    acceptance_proofs = []
    for proof in acceptance_hooks.get('code_proofs', []):
        acceptance_proofs.append(f"Proof: {proof}")
    for test in acceptance_hooks.get('test_requirements', []):
        acceptance_proofs.append(f"Test: {test}")
    
    # Build in_scope from evidence plan
    evidence_plan = meta.get('evidence_plan', {})
    in_scope = evidence_plan.get('final_artifacts', ["Implementation per hypothesis"])
    
    # Build non_goals from constraints
    constraints = meta.get('constraints', [])
    non_goals = [f"Beyond constraint: {c}" for c in constraints[:2]] if constraints else ["[Out of scope item]"]
    
    design_content = f'''---
schema_version: "0.1"
dossier_id: "{design_id}"
product_id: "{product_id}"
owner: "nexus"
status: "draft"
created_at: "{date_iso}"
hypothesis:
  problem: "{meta.get('hypothesis', {}).get('statement', '[Problem from science dossier]')}"
  claim: "Converting science hypothesis to implementation."
  falsification: "{meta.get('hypothesis', {}).get('null_hypothesis', '[Falsification criteria]')}"
mvp_boundary:
  in_scope:
'''
    for item in in_scope[:3]:
        design_content += f'    - "{item}"\n'
    design_content += '''  non_goals:
'''
    for ng in non_goals[:2]:
        design_content += f'    - "{ng}"\n'
    design_content += f'''acceptance_proofs:
'''
    for proof in acceptance_proofs[:4]:
        design_content += f'  - "{proof}"\n'
    design_content += f'''evidence:
  links: []
  science_source: "{meta.get('dossier_id')}"
constitution_refs:
'''
    for ref in meta.get('constitution_refs', ['constitution.md']):
        design_content += f'  - "{ref}"\n'
    design_content += f'''---

# Design Dossier: {product_id} (from Science)

**Source Science Dossier:** `{path}`

## 1. Context & Problem
{meta.get('hypothesis', {}).get('statement', '[From science dossier hypothesis]')}

## 2. Hypothesis
{meta.get('hypothesis', {}).get('statement', '[Hypothesis]')}

**Falsification:** {meta.get('hypothesis', {}).get('null_hypothesis', '[From science dossier]')}

## 3. MVP Definition
Derived from science evidence plan.

## 4. Evidence Plan
Validation method: {evidence_plan.get('validation_method', '[From science dossier]')}
'''
    
    design_file.parent.mkdir(parents=True, exist_ok=True)
    design_file.write_text(design_content)
    
    click.echo(f"Created Design Dossier: {design_file}")
    click.echo(f"  Source: {path}")
    click.echo(f"  Product ID: {product_id}")
    click.echo(f"\nNext: codemonkeys dossier validate {design_file}")

