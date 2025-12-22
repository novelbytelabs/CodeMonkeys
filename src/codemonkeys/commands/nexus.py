import click
import sys
import subprocess
from rich.console import Console

console = Console()

@click.group()
def nexus():
    """Nexus Executive operations."""
    pass

@nexus.command()
@click.option('--decision', help='Process specific decision ID')
@click.option('--dry-run', is_flag=True, help='Preview only')
def exec(decision, dry_run):
    """Execute pending Nexus decisions."""
    console.print("[bold blue]Code Monkeys Factory :: Nexus Execution[/bold blue]")
    
    cmd = ["python", "scripts/nexus_executor.py"]
    if decision:
        cmd.extend(["--decision", decision])
    if dry_run:
        cmd.append("--dry-run")
        
    try:
        result = subprocess.run(cmd, check=False)
        if result.returncode != 0:
            sys.exit(result.returncode)
    except Exception as e:
        console.print(f"[bold red]Error running Nexus Executor:[/bold red] {e}")
        sys.exit(1)
