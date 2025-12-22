#!/usr/bin/env python3
"""
Silverback Validator (Bootstrap)

Validates that specs are implementation-ready, run artifacts are valid,
and Nexus inbox/outbox artifacts conform to their schemas.

Usage:
    python scripts/silverback_validate.py --spec specs/000-dash-mvp/spec.md
    python scripts/silverback_validate.py --run-artifact dash/runs/codemonkeys-dash/last_run.json
    python scripts/silverback_validate.py --nexus  # Validate Nexus inbox/outbox
    python scripts/silverback_validate.py --all

Exit codes:
    0: All validations passed
    1: Validation errors found
    2: Internal error
"""
import argparse
import json
import re
import sys
from pathlib import Path

try:
    from jsonschema import validate, ValidationError
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False


# Mandatory spec sections that must not be blank
MANDATORY_SECTIONS = [
    "Intent",
    "User Stories",
    "Functional Requirements",
    "Acceptance Criteria",
    "Owner & Authority",
    "Budget & Stop Conditions",
    "Constraints & Non-goals",
    "Evidence Plan",
    "Traceability Map",
]

DASH_SCHEMA_DIR = Path("dash/schemas")
NEXUS_SCHEMA_DIR = Path("nexus/schemas")
NEXUS_INBOX_DIR = Path("nexus/inbox")
NEXUS_OUTBOX_DIR = Path("nexus/outbox")


class ValidationResult:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def error(self, msg):
        self.errors.append(msg)
        print(f"[ERROR] {msg}")

    def warning(self, msg):
        self.warnings.append(msg)
        print(f"[WARN] {msg}")

    def ok(self, msg):
        print(f"[OK] {msg}")

    @property
    def passed(self):
        return len(self.errors) == 0


def validate_spec(spec_path: Path, result: ValidationResult):
    """Validate that a spec file has non-empty mandatory sections, a valid Dossier, and correct Governance."""
    if not spec_path.exists():
        result.error(f"Spec not found: {spec_path}")
        return

    content = spec_path.read_text()
    
    # 1. Dossier & Constitution Header Gate
    dossier_match = re.search(r"^Dossier:\s*(DOS-[\w-]+)", content, re.MULTILINE)
    const_match = re.search(r"^Constitution:\s*([\w\.]+)", content, re.MULTILINE)
    legacy_match = re.search(r"^Legacy-Spec:\s*true", content, re.MULTILINE | re.IGNORECASE)
    
    if dossier_match:
        dossier_id = dossier_match.group(1)
        # Try to find the dossier file (fuzzy match)
        dossier_files = list(Path("docs/dossiers").glob(f"{dossier_id}*.md"))
        
        if dossier_files:
            dossier_path = dossier_files[0]
            result.ok(f"Dossier reference found: {dossier_id} -> {dossier_path}")
            
            # Validate Dossier Content & Governance
            try:
                import frontmatter
                post = frontmatter.load(dossier_path)
                meta = post.metadata
                
                # Check for Constitution Refs
                refs = meta.get("constitution_refs", [])
                if not refs:
                    result.error(f"Dossier {dossier_id} missing 'constitution_refs' (must include constitution.md)")
                    _escalate_to_nexus_silverback(result, dossier_path, "Missing constitution_refs")
                elif "constitution.md" not in refs:
                     result.error(f"Dossier {dossier_id} must reference 'constitution.md'")
                     _escalate_to_nexus_silverback(result, dossier_path, "Missing constitution.md reference")
                else:
                    # Check if referenced docs exist
                    missing_refs = [r for r in refs if not Path(r).exists()]
                    if missing_refs:
                         result.error(f"Dossier {dossier_id} references missing docs: {missing_refs}")
                    else:
                         result.ok(f"Dossier {dossier_id} governance valid")

                if not meta.get("acceptance_proofs"):
                    result.error(f"Dossier {dossier_id} missing acceptance_proofs")
            except Exception as e:
                 result.error(f"Failed to load dossier {dossier_id}: {e}")
        else:
             result.error(f"Referenced Dossier not found: {dossier_id}")
        
        # Check for Constitution Header in Spec
        if not const_match:
             result.error("Spec missing 'Constitution: constitution.md' header")

    elif legacy_match:
        result.warning(f"Legacy Spec bypass: {spec_path.name}")
    else:
        # Bootstrap Exceptions
        if "000-dash-mvp" in str(spec_path) or "001-factory-cli" in str(spec_path):
             result.warning(f"Bootstrap Spec allowed without Dossier: {spec_path.name}")
        else:
             result.error(f"Spec missing 'Dossier: DOS-...' header: {spec_path.name}")

    for section in MANDATORY_SECTIONS:
        # Match "## Section" OR "## 1. Section"
        pattern = rf"##+\s+(\d+\.\s+)?{re.escape(section)}"
        match = re.search(pattern, content, re.IGNORECASE)
        
        if not match:
            result.error(f"Missing section: '{section}'")
            continue

        section_start = match.end()
        next_section = re.search(r"\n##+ ", content[section_start:])
        section_end = section_start + next_section.start() if next_section else len(content)
        section_content = content[section_start:section_end].strip()

        placeholder_patterns = [
            r"\[.*?\]",
            r"<.*?>",
            r"ACTION REQUIRED",
            r"NEEDS CLARIFICATION",
        ]

        cleaned = section_content
        for p in placeholder_patterns:
            cleaned = re.sub(p, "", cleaned)
        
        cleaned = re.sub(r"[#*_\-|`]", "", cleaned).strip()
        
        if len(cleaned) < 20:
            result.warning(f"Section '{section}' appears to be placeholder-only")
        else:
            result.ok(f"Section '{section}' has content")

def _escalate_to_nexus_silverback(result, context, reason):
    """Create a Nexus request for clarification (internal helper)."""
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    req_file = Path(f"nexus/inbox/req_{timestamp}_governance_escalation.json")
    
    payload = {
        "schema_version": "0.1",
        "request_id": f"req_{timestamp}",
        "type": "clarification_required",
        "source": "silverback_validator",
        "created_at": datetime.now().isoformat(),
        "status": "pending",
        "priority": "high",
        "payload": {
            "description": f"Governance check failed: {reason}",
            "context": str(context)
        }
    }
    
    try:
        req_file.write_text(json.dumps(payload, indent=2))
        result.warning(f"Nexus escalation created: {req_file}")
    except Exception as e:
        result.error(f"Failed to create Nexus escalation: {e}")


def validate_run_artifact(artifact_path: Path, result: ValidationResult):
    """Validate a run artifact against its schema and check evidence."""
    if not artifact_path.exists():
        result.error(f"Run artifact not found: {artifact_path}")
        return None

    try:
        data = json.loads(artifact_path.read_text())
    except json.JSONDecodeError as e:
        result.error(f"Invalid JSON in {artifact_path}: {e}")
        return None

    result.ok(f"JSON parsed: {artifact_path}")

    schema_path = DASH_SCHEMA_DIR / "last_run.schema.json"
    if HAS_JSONSCHEMA and schema_path.exists():
        try:
            schema = json.loads(schema_path.read_text())
            validate(instance=data, schema=schema)
            result.ok("Schema validation passed")
        except ValidationError as e:
            result.error(f"Schema validation failed: {e.message}")
    else:
        result.warning("Schema validation skipped (jsonschema not available or schema missing)")

    evidence_paths = data.get("evidence", {}).get("paths", [])
    if not evidence_paths:
        result.warning("No evidence paths in artifact")
    else:
        base_dir = Path("dash")
        for ep in evidence_paths:
            full_path = base_dir / ep
            if full_path.exists():
                result.ok(f"Evidence exists: {ep}")
            else:
                result.error(f"Evidence missing: {ep}")

    return data


def validate_nexus_artifact(artifact_path: Path, schema_path: Path, artifact_type: str, result: ValidationResult):
    """Validate a Nexus artifact (inbox or outbox) against its schema."""
    if not artifact_path.exists():
        result.error(f"Nexus {artifact_type} not found: {artifact_path}")
        return None

    try:
        data = json.loads(artifact_path.read_text())
    except json.JSONDecodeError as e:
        result.error(f"Invalid JSON in {artifact_path}: {e}")
        return None

    result.ok(f"JSON parsed: {artifact_path}")

    # Validate schema version
    if data.get("schema_version") != "0.1":
        result.warning(f"Unexpected schema version in {artifact_path}: {data.get('schema_version')}")

    # Schema validation
    if HAS_JSONSCHEMA and schema_path.exists():
        try:
            schema = json.loads(schema_path.read_text())
            validate(instance=data, schema=schema)
            result.ok(f"Schema validation passed: {artifact_path.name}")
        except ValidationError as e:
            result.error(f"Schema validation failed for {artifact_path.name}: {e.message}")
    else:
        result.warning(f"Schema validation skipped for {artifact_path.name}")

    # For decisions, check governance compliance field
    if artifact_type == "outbox" and "governance_check" in data:
        gc = data["governance_check"]
        if gc.get("compliant"):
            result.ok(f"Governance compliant: {artifact_path.name}")
        else:
            violations = gc.get("violations", [])
            result.warning(f"Governance violations in {artifact_path.name}: {violations}")

    return data


def validate_nexus_inbox(result: ValidationResult):
    """Validate all Nexus inbox artifacts."""
    if not NEXUS_INBOX_DIR.exists():
        result.warning("Nexus inbox directory not found")
        return

    schema_path = NEXUS_SCHEMA_DIR / "request.schema.json"
    files = list(NEXUS_INBOX_DIR.glob("*.json"))
    
    if not files:
        result.warning("No inbox files found")
        return

    for filepath in files:
        validate_nexus_artifact(filepath, schema_path, "inbox", result)


def validate_nexus_outbox(result: ValidationResult):
    """Validate all Nexus outbox artifacts."""
    if not NEXUS_OUTBOX_DIR.exists():
        result.warning("Nexus outbox directory not found")
        return

    schema_path = NEXUS_SCHEMA_DIR / "decision.schema.json"
    files = list(NEXUS_OUTBOX_DIR.glob("*.json"))
    
    if not files:
        result.warning("No outbox files found")
        return

    for filepath in files:
        validate_nexus_artifact(filepath, schema_path, "outbox", result)


def validate_all(result: ValidationResult):
    """Run all validations for the current project."""
    print("\n=== Silverback Validation (Bootstrap) ===\n")

    # Validate specs
    specs_dir = Path("specs")
    if specs_dir.exists():
        for spec_dir in specs_dir.iterdir():
            if spec_dir.is_dir():
                spec_file = spec_dir / "spec.md"
                if spec_file.exists():
                    print(f"\n--- Validating spec: {spec_file} ---")
                    validate_spec(spec_file, result)

    # Validate run artifacts
    runs_dir = Path("dash/runs")
    if runs_dir.exists():
        for product_dir in runs_dir.iterdir():
            if product_dir.is_dir():
                last_run = product_dir / "last_run.json"
                if last_run.exists():
                    print(f"\n--- Validating artifact: {last_run} ---")
                    validate_run_artifact(last_run, result)

    # Validate Nexus inbox
    print("\n--- Validating Nexus inbox ---")
    validate_nexus_inbox(result)

    # Validate Nexus outbox
    print("\n--- Validating Nexus outbox ---")
    validate_nexus_outbox(result)


def main():
    parser = argparse.ArgumentParser(description="Silverback Validator")
    parser.add_argument("--spec", help="Validate a specific spec file")
    parser.add_argument("--run-artifact", help="Validate a specific run artifact")
    parser.add_argument("--nexus", action="store_true", help="Validate Nexus inbox/outbox only")
    parser.add_argument("--all", action="store_true", help="Validate all specs and artifacts")
    args = parser.parse_args()

    result = ValidationResult()

    if args.spec:
        print(f"\n--- Validating spec: {args.spec} ---")
        validate_spec(Path(args.spec), result)
    elif args.run_artifact:
        print(f"\n--- Validating artifact: {args.run_artifact} ---")
        validate_run_artifact(Path(args.run_artifact), result)
    elif args.nexus:
        print("\n=== Silverback Validation (Nexus) ===\n")
        print("--- Validating Nexus inbox ---")
        validate_nexus_inbox(result)
        print("\n--- Validating Nexus outbox ---")
        validate_nexus_outbox(result)
    elif args.all:
        validate_all(result)
    else:
        validate_all(result)

    # Summary
    print("\n=== Summary ===")
    print(f"Errors: {len(result.errors)}")
    print(f"Warnings: {len(result.warnings)}")

    if result.passed:
        print("\n✅ Silverback validation PASSED")
        return 0
    else:
        print("\n❌ Silverback validation FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
