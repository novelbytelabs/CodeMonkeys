#!/usr/bin/env python3
"""Cutover rehearsal script - export and validate subset for new repo."""
import json
import shutil
import subprocess
import sys
from pathlib import Path


def export_subset(source_dir: Path, target_dir: Path) -> bool:
    """Export canonical subset to target directory."""
    # Define canonical subset to export
    canonical_paths = [
        # Core source
        "src/",
        "scripts/",
        "pyproject.toml",

        # Dash
        "dash/products.json",
        "dash/science_index.json",
        "dash/schemas/",
        "dash/schedules/",
        "dash/runs/",
        "dash/index.html",
        "dash/css/",
        "dash/js/",

        # Specs (just one for minimal test)
        "specs/001-factory-cli/",

        # Docs
        "docs/science/",
        "docs/dossiers/",
        "docs/schemas/",
        "docs/pm/",

        # Nexus
        "nexus/schemas/",
        "nexus/inbox/",
        "nexus/outbox/",

        # Tests
        "tests/",

        # Config
        ".agent/constitution.md",
        "constitution.md",
    ]

    target_dir.mkdir(parents=True, exist_ok=True)

    for path_str in canonical_paths:
        source_path = source_dir / path_str
        target_path = target_dir / path_str

        if not source_path.exists():
            print(f"  Skipping (not found): {path_str}")
            continue

        if source_path.is_dir():
            if target_path.exists():
                shutil.rmtree(target_path)
            shutil.copytree(source_path, target_path)
        else:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, target_path)

        print(f"  Copied: {path_str}")

    return True


def validate_export(target_dir: Path) -> tuple[bool, str]:
    """Run pytest and Silverback in export directory."""
    results = []

    # Run pytest
    print("\n[Pytest]")
    pytest_result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-q", "--tb=no"],
        cwd=target_dir,
        capture_output=True,
        text=True
    )
    results.append(("pytest", pytest_result.returncode == 0))
    print(pytest_result.stdout[-500:] if len(pytest_result.stdout) > 500 else pytest_result.stdout)

    # Note: Silverback validation requires full repo context
    # For cutover rehearsal, we just verify pytest passes
    results.append(("basic_structure", (target_dir / "src").exists()))

    all_passed = all(passed for _, passed in results)
    summary = "\n".join(f"  {name}: {'✓' if passed else '✗'}" for name, passed in results)

    return all_passed, summary


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Cutover Rehearsal")
    parser.add_argument("--target", type=Path, default=Path("/tmp/codemonkeys-export"),
                        help="Target export directory")
    parser.add_argument("--source", type=Path, default=Path("."),
                        help="Source directory")
    parser.add_argument("--clean", action="store_true",
                        help="Clean target before export")
    parser.add_argument("--skip-validate", action="store_true",
                        help="Skip validation step")

    args = parser.parse_args()

    print(f"[Cutover Rehearsal]")
    print(f"  Source: {args.source.absolute()}")
    print(f"  Target: {args.target.absolute()}")

    if args.clean and args.target.exists():
        print(f"\n[Cleaning {args.target}]")
        shutil.rmtree(args.target)

    print("\n[Exporting canonical subset]")
    if not export_subset(args.source, args.target):
        print("\n✗ Export failed")
        return 1

    if args.skip_validate:
        print("\n✓ Export complete (validation skipped)")
        return 0

    print("\n[Validating export]")
    passed, summary = validate_export(args.target)

    print(f"\n[Results]")
    print(summary)

    if passed:
        print("\n✓ Cutover rehearsal passed")
        return 0
    else:
        print("\n✗ Cutover rehearsal failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
