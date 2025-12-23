"""Doctor command - onboarding health check for Code Monkeys environment.

Split into:
- Core checks: deterministic, testable, cause hard fail
- Environment hints: best-effort, cause soft warn only
"""
import json
import os
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

console = Console()


# Required paths relative to repo root
REQUIRED_PATHS = [
    "constitution.md",
    "dash/products.json",
    "dash/schemas/last_run.schema.json",
    "nexus/schemas/request.schema.json",
    "nexus/schemas/decision.schema.json",
]

# Required Python packages
REQUIRED_PACKAGES = [
    "click",
    "rich",
    "pytest",
    "jsonschema",
]


def check_python_version() -> tuple[bool, str]:
    """Check Python version >= 3.10."""
    version = sys.version_info
    if version >= (3, 10):
        return True, f"Python {version.major}.{version.minor}.{version.micro}"
    return False, f"Python {version.major}.{version.minor} (need >= 3.10)"


def check_required_packages() -> tuple[bool, str]:
    """Check all required packages are importable."""
    missing = []
    for pkg in REQUIRED_PACKAGES:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)

    if missing:
        return False, f"Missing: {', '.join(missing)}"
    return True, "All packages available"


def check_required_paths() -> tuple[bool, str]:
    """Check all required repo paths exist."""
    missing = []
    for p in REQUIRED_PATHS:
        if not Path(p).exists():
            missing.append(p)

    if missing:
        return False, f"Missing: {', '.join(missing[:3])}{'...' if len(missing) > 3 else ''}"
    return True, f"{len(REQUIRED_PATHS)} paths found"


def check_products_json() -> tuple[bool, str]:
    """Check products.json is valid and parseable."""
    products_path = Path("dash/products.json")
    if not products_path.exists():
        return False, "File not found"

    try:
        data = json.loads(products_path.read_text())
        products = data.get("products", [])
        return True, f"{len(products)} products defined"
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"


def check_git_remote() -> tuple[bool, str]:
    """Check git remote is configured."""
    import subprocess
    try:
        result = subprocess.run(
            ["git", "remote", "-v"],
            capture_output=True, text=True, check=True
        )
        if "origin" in result.stdout:
            # Extract URL
            for line in result.stdout.split("\n"):
                if "origin" in line and "(fetch)" in line:
                    url = line.split()[1]
                    return True, url
            return True, "origin configured"
        return False, "No 'origin' remote"
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False, "Git not available"


def check_conda_env() -> tuple[bool, str]:
    """Check if helios-gpu-118 conda env is active (soft warn)."""
    env_name = os.environ.get("CONDA_DEFAULT_ENV", "")
    if env_name == "helios-gpu-118":
        return True, "helios-gpu-118 active"
    elif env_name:
        return False, f"Active: {env_name} (expected helios-gpu-118)"
    else:
        return False, "No conda env active"


def run_core_checks() -> list[tuple[str, bool, str]]:
    """Run core checks (hard fail on error)."""
    checks = [
        ("Python Version", *check_python_version()),
        ("Required Packages", *check_required_packages()),
        ("Required Paths", *check_required_paths()),
        ("Products Registry", *check_products_json()),
        ("Git Remote", *check_git_remote()),
    ]
    return checks


def run_env_checks() -> list[tuple[str, bool, str]]:
    """Run environment checks (soft warn only)."""
    checks = [
        ("Conda Environment", *check_conda_env()),
    ]
    return checks


@click.command()
@click.option("--verbose", "-v", is_flag=True, help="Show detailed output")
def doctor(verbose):
    """Check environment health for Code Monkeys development."""
    console.print("\n[bold blue]Code Monkeys Factory :: Doctor[/bold blue]\n")

    # Run core checks
    core_results = run_core_checks()
    env_results = run_env_checks()

    # Display results
    table = Table(title="Health Checks")
    table.add_column("Check", style="cyan")
    table.add_column("Status", justify="center")
    table.add_column("Details")

    errors = 0
    warnings = 0

    for name, passed, detail in core_results:
        if passed:
            status = "[green]✓[/green]"
        else:
            status = "[red]✗[/red]"
            errors += 1
        table.add_row(name, status, detail)

    for name, passed, detail in env_results:
        if passed:
            status = "[green]✓[/green]"
        else:
            status = "[yellow]⚠[/yellow]"
            warnings += 1
        table.add_row(name, status, detail)

    console.print(table)
    console.print()

    # Summary
    if errors > 0:
        console.print(f"[bold red]✗ {errors} error(s) found[/bold red]")
        console.print("  Fix the errors above before proceeding.")
        sys.exit(1)
    elif warnings > 0:
        console.print(f"[bold yellow]⚠ {warnings} warning(s)[/bold yellow]")
        console.print("  [dim]Warnings are informational and won't block work.[/dim]")
        console.print("\n[bold green]✓ Core checks passed[/bold green]")
        sys.exit(0)
    else:
        console.print("[bold green]✓ All checks passed[/bold green]")
        sys.exit(0)
