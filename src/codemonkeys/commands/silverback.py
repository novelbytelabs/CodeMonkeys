import click
import sys
import subprocess
from rich.console import Console

console = Console()

@click.command()
@click.option('--all', 'validate_all', is_flag=True, help='Validate everything')
@click.option('--nexus', is_flag=True, help='Validate Nexus only')
@click.option('--target', help='Validate specific file')
def silverback(validate_all, nexus, target):
    """Run Silverback validation."""
    console.print("[bold blue]Code Monkeys Factory :: Silverback Validation[/bold blue]")
    
    cmd = [sys.executable, "scripts/silverback_validate.py"]
    if validate_all:
        cmd.append("--all")
    if nexus:
        cmd.append("--nexus")
    if target:
        cmd.append("--spec")
        cmd.append(target)
        
    try:
        result = subprocess.run(cmd, check=False)
        if result.returncode != 0:
            sys.exit(result.returncode)
    except Exception as e:
        console.print(f"[bold red]Error running Silverback:[/bold red] {e}")
        sys.exit(1)
