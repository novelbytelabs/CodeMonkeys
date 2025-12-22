
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
