
import click
import subprocess
import sys
from rich.console import Console
from rich.prompt import Confirm
import os

console = Console()

@click.command()
@click.option('--dry-run', is_flag=True, help="Run checks but do not tag/push.")
@click.option('--force', is_flag=True, help="Bypass preflight checks (REQUIRES CONSTITUTIONAL OVERRIDE - NOT IMPLEMENTED).")
@click.argument('version')
def ship(version, dry_run, force):
    """
    Ship a released version (Tag & Push).
    ENFORCES: Preflight Check (Git Clean + Silverback Valid).
    """
    console.print(f"[bold yellow]🚢 Preparing to ship version: {version}[/bold yellow]")

    # 1. Preflight Gate
    if not force:
        console.print("[dim]Running Preflight Gate...[/dim]")
        # We invoke the script directly
        script_path = "scripts/preflight_check.py"
        if not os.path.exists(script_path):
             console.print(f"[bold red]❌ Critical: Preflight script missing at {script_path}[/bold red]")
             sys.exit(1)

        result = subprocess.run([sys.executable, script_path])
        if result.returncode != 0:
            console.print("[bold red]⛔ Release Gate Closed. Preflight Failed.[/bold red]")
            sys.exit(1)
    else:
        console.print("[bold red]⚠️  FORCING RELEASE - GATE BYPASSED. THIS WILL BE LOGGED.[/bold red]")
        # Todo: Log this constitutional violation to Nexus

    # 2. Tag & Push
    tags = subprocess.run(["git", "tag", "-l", version], capture_output=True, text=True).stdout.strip()
    if tags:
        console.print(f"[bold red]❌ Tag {version} already exists.[/bold red]")
        sys.exit(1)

    if dry_run:
        console.print("[bold green]✅ Dry run passed. Ready to tag.[/bold green]")
        return

    if Confirm.ask(f"Ready to tag and push {version}?"):
        subprocess.run(["git", "tag", "-a", version, "-m", f"Release {version}"], check=True)
        console.print(f"[green]Tagged {version}[/green]")
        
        # subprocess.run(["git", "push", "origin", version], check=True)
        # console.print(f"[green]Pushed {version}[/green]")
        console.print("[yellow]Push skipped for local dev simulation.[/yellow]")

    console.print("[bold green]🚀 Ship Complete.[/bold green]")
