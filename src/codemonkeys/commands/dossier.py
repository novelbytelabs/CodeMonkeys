import click
import frontmatter
import json
import re
import sys
from pathlib import Path
from datetime import datetime
from rich.console import Console
from jsonschema import validate as json_validate, ValidationError as JsonValidationError

console = Console()

SCHEMA_PATH = Path("docs/schemas/design_dossier.schema.json")
TEMPLATE_PATH = Path("docs/pm/DESIGN_DOSSIER_TEMPLATE.md")
DOSSIERS_DIR = Path("docs/dossiers")
SPECS_DIR = Path("specs")
NEXUS_INBOX = Path("nexus/inbox")

def create_nexus_escalation(dossier_path, errors):
    """Create a Nexus request for clarification."""
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    req_id = f"req_{timestamp}_dossier_escalation"
    
    payload = {
        "schema_version": "0.1",
        "request_id": req_id,
        "type": "clarification_required",
        "source": "silverback-dossier-validator",
        "created_at": f"{datetime.utcnow().isoformat()}Z",
        "priority": "high",
        "status": "pending",
        "payload": {
            "dossier": str(dossier_path),
            "validation_errors": errors,
            "instructions": "Please update the Dossier with missing proofs or fields."
        }
    }
    
    out_path = NEXUS_INBOX / f"{req_id}.json"
    out_path.write_text(json.dumps(payload, indent=2))
    console.print(f"[yellow]Nexus escalation created: {out_path}[/yellow]")

@click.group()
def dossier():
    """Manage Design Dossiers."""
    pass

@dossier.command()
@click.argument('path', type=click.Path(exists=True))
def validate(path):
    """Validate a Design Dossier (Markdown + YAML)."""
    console.print(f"[blue]Validating Dossier: {path}[/blue]")
    path_obj = Path(path)
    
    try:
        post = frontmatter.load(path)
    except Exception as e:
        console.print(f"[red]Failed to parse YAML front-matter: {e}[/red]")
        sys.exit(1)
        
    errors = []
    
    # Schema Validation
    if SCHEMA_PATH.exists():
        try:
            schema = json.loads(SCHEMA_PATH.read_text())
            json_validate(instance=post.metadata, schema=schema)
            console.print("[green]YAML Schema Valid[/green]")
        except JsonValidationError as e:
            msg = f"Schema Error: {e.message}"
            console.print(f"[red]{msg}[/red]")
            errors.append(msg)
    else:
        console.print("[yellow]Schema not found, skipping validation[/yellow]")

    # Content Validation (Proof Check)
    proofs = post.metadata.get("acceptance_proofs", [])
    if not proofs:
        msg = "Missing 'acceptance_proofs' in YAML."
        errors.append(msg)
    else:
        # Check for placeholder content
        for p in proofs:
            if "[" in p and "]" in p:
                 msg = f"Placeholder detected in proofs: {p}"
                 errors.append(msg)

    if errors:
        console.print("[bold red]Validation Failed[/bold red]")
        create_nexus_escalation(path_obj, errors)
        sys.exit(1)
    else:
        console.print("[bold green]Dossier Valid[/bold green]")

@dossier.command()
@click.argument('product_id')
def new(product_id):
    """Create a new Dossier from template."""
    if not TEMPLATE_PATH.exists():
        console.print("[red]Template not found![/red]")
        sys.exit(1)
        
    content = TEMPLATE_PATH.read_text()
    
    # Simple template substitution (could be more robust)
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    dos_id = f"DOS-{datetime.utcnow().strftime('%Y%m%d')}-{product_id}"
    
    content = content.replace("[YYYY-MM-DD]", date_str)
    content = content.replace("DOS-[YYYYMMDD-ID]", dos_id)
    content = content.replace("[product-slug]", product_id)
    
    out_file = DOSSIERS_DIR / f"{dos_id}.md"
    if out_file.exists():
        console.print(f"[red]File exists: {out_file}[/red]")
        sys.exit(1)
        
    out_file.write_text(content)
    console.print(f"[green]Created Dossier: {out_file}[/green]")

@dossier.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--spec-id', required=True, help='ID for the new spec (e.g. 003)')
def to_spec(path, spec_id):
    """Generate a Spec skeleton from a Dossier."""
    post = frontmatter.load(path)
    meta = post.metadata
    
    product_slug = meta.get('product_id', 'unknown')
    spec_dir = SPECS_DIR / f"{spec_id}-{product_slug}"
    spec_file = spec_dir / "spec.md"
    
    if spec_file.exists():
        console.print(f"[red]Spec already exists: {spec_file}[/red]")
        sys.exit(1)
        
    spec_dir.mkdir(parents=True, exist_ok=True)
    
    hypothesis = meta.get('hypothesis', {})
    
    # Spec Scaffold
    content = f"""# Spec: {product_slug}

Dossier: {meta.get('dossier_id')}
Status: Draft
Owner: {meta.get('owner')}
Epic: {product_slug}

## 1. Intent
{hypothesis.get('problem', 'Problem statement...')}
{hypothesis.get('claim', 'Hypothesis...')}

## 2. User Stories
- **As a User**, I want [feature] so that [benefit].

## 3. Functional Requirements
1.  **Requirement 1**: ...

## 4. Acceptance Criteria
{chr(10).join([f"1. {p}" for p in meta.get('acceptance_proofs', [])])}

## 5. Owner & Authority
- **Feature Owner**: Nexus Agent
- **Governance**: Inherits from Dossier {meta.get('dossier_id')}.
- **Approval**: Human Operator.

## 6. Budget & Stop Conditions
- **Budget**: Standard.
- **Stop Condition**: Kill switch.

## 7. Constraints & Non-goals
**Non-goals**:
{chr(10).join([f"- {ng}" for ng in meta.get('mvp_boundary', {}).get('non_goals', [])])}

## 8. Evidence Plan
- **Artifacts**: Standard run artifacts.

## 9. Traceability Map
- `docs/dossiers/{Path(path).name}` -> `specs/{spec_id}-{product_slug}/spec.md`
"""
    spec_file.write_text(content)
    console.print(f"[green]Generated Spec: {spec_file}[/green]")
