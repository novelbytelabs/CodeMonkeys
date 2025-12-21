#!/usr/bin/env python3
"""
Silverback Validator (Bootstrap)

Validates that specs are implementation-ready and run artifacts are valid.

Usage:
    python scripts/silverback_validate.py --spec specs/000-dash-mvp/spec.md
    python scripts/silverback_validate.py --run-artifact dash/runs/codemonkeys-dash/last_run.json
    python scripts/silverback_validate.py --all

Exit codes:
    0: All validations passed
    1: Validation errors found
    2: Internal error
"""
import argparse
import json
import os
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

SCHEMA_DIR = Path("dash/schemas")


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
    """Validate that a spec file has non-empty mandatory sections."""
    if not spec_path.exists():
        result.error(f"Spec not found: {spec_path}")
        return

    content = spec_path.read_text()

    for section in MANDATORY_SECTIONS:
        # Match section header (## or ###)
        pattern = rf"##+ {re.escape(section)}"
        match = re.search(pattern, content, re.IGNORECASE)
        
        if not match:
            result.error(f"Missing section: '{section}'")
            continue

        # Check if section has content (not just placeholders)
        section_start = match.end()
        next_section = re.search(r"\n##+ ", content[section_start:])
        section_end = section_start + next_section.start() if next_section else len(content)
        section_content = content[section_start:section_end].strip()

        # Check for blank or placeholder-only content
        placeholder_patterns = [
            r"\[.*?\]",  # [placeholder]
            r"<.*?>",    # <placeholder>
            r"ACTION REQUIRED",
            r"NEEDS CLARIFICATION",
        ]

        cleaned = section_content
        for p in placeholder_patterns:
            cleaned = re.sub(p, "", cleaned)
        
        # Remove markdown formatting and check if anything remains
        cleaned = re.sub(r"[#*_\-|`]", "", cleaned).strip()
        
        if len(cleaned) < 20:  # Too short to be real content
            result.warning(f"Section '{section}' appears to be placeholder-only")
        else:
            result.ok(f"Section '{section}' has content")


def validate_run_artifact(artifact_path: Path, result: ValidationResult):
    """Validate a run artifact against its schema and check evidence."""
    if not artifact_path.exists():
        result.error(f"Run artifact not found: {artifact_path}")
        return None

    # Load artifact
    try:
        data = json.loads(artifact_path.read_text())
    except json.JSONDecodeError as e:
        result.error(f"Invalid JSON in {artifact_path}: {e}")
        return None

    result.ok(f"JSON parsed: {artifact_path}")

    # Schema validation
    schema_path = SCHEMA_DIR / "last_run.schema.json"
    if HAS_JSONSCHEMA and schema_path.exists():
        try:
            schema = json.loads(schema_path.read_text())
            validate(instance=data, schema=schema)
            result.ok("Schema validation passed")
        except ValidationError as e:
            result.error(f"Schema validation failed: {e.message}")
    else:
        result.warning("Schema validation skipped (jsonschema not available or schema missing)")

    # Check evidence paths exist
    evidence_paths = data.get("evidence", {}).get("paths", [])
    if not evidence_paths:
        result.warning("No evidence paths in artifact")
    else:
        base_dir = Path("dash")  # Evidence paths are relative to dash/
        for ep in evidence_paths:
            full_path = base_dir / ep
            if full_path.exists():
                result.ok(f"Evidence exists: {ep}")
            else:
                result.error(f"Evidence missing: {ep}")

    return data


def validate_all(result: ValidationResult):
    """Run all validations for the current project."""
    print("\n=== Silverback Validation (Bootstrap) ===\n")

    # Find specs
    specs_dir = Path("specs")
    if specs_dir.exists():
        for spec_dir in specs_dir.iterdir():
            if spec_dir.is_dir():
                spec_file = spec_dir / "spec.md"
                if spec_file.exists():
                    print(f"\n--- Validating spec: {spec_file} ---")
                    validate_spec(spec_file, result)

    # Find run artifacts
    runs_dir = Path("dash/runs")
    if runs_dir.exists():
        for product_dir in runs_dir.iterdir():
            if product_dir.is_dir():
                last_run = product_dir / "last_run.json"
                if last_run.exists():
                    print(f"\n--- Validating artifact: {last_run} ---")
                    validate_run_artifact(last_run, result)


def main():
    parser = argparse.ArgumentParser(description="Silverback Validator")
    parser.add_argument("--spec", help="Validate a specific spec file")
    parser.add_argument("--run-artifact", help="Validate a specific run artifact")
    parser.add_argument("--all", action="store_true", help="Validate all specs and artifacts")
    args = parser.parse_args()

    result = ValidationResult()

    if args.spec:
        print(f"\n--- Validating spec: {args.spec} ---")
        validate_spec(Path(args.spec), result)
    elif args.run_artifact:
        print(f"\n--- Validating artifact: {args.run_artifact} ---")
        validate_run_artifact(Path(args.run_artifact), result)
    elif args.all:
        validate_all(result)
    else:
        # Default: validate all
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
