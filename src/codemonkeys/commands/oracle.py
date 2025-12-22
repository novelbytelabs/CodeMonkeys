"""Oracle command - work orchestration and execution."""
import subprocess
import sys
from pathlib import Path

import click
from rich.console import Console

console = Console()


@click.group()
def oracle():
    """Oracle - work order planning and execution."""
    pass


@oracle.command()
@click.option("--budget", default=3, type=int, help="Max work orders to generate")
@click.option("--stdout", is_flag=True, help="Output to stdout instead of files")
@click.option("--output-dir", type=click.Path(), default="nexus/work_orders", help="Output directory")
@click.option("--deterministic", is_flag=True, help="Use deterministic job IDs for testing")
def plan(budget: int, stdout: bool, output_dir: str, deterministic: bool):
    """Generate bounded, prioritized work orders."""
    console.print("[bold blue]Code Monkeys Factory :: Oracle Plan[/bold blue]")
    
    cmd = [sys.executable, "scripts/oracle_planner.py", "--budget", str(budget)]
    
    if stdout:
        cmd.append("--stdout")
    else:
        cmd.extend(["--output-dir", output_dir])
    
    if deterministic:
        cmd.append("--deterministic")
    
    result = subprocess.run(cmd, capture_output=False)
    
    raise SystemExit(result.returncode)


@oracle.command()
@click.option("--budget", default=3, type=int, help="Max work orders to execute")
@click.option("--dry-run", is_flag=True, help="Preview execution without making changes")
@click.option("--work-orders-dir", type=click.Path(), default="nexus/work_orders", help="Work orders directory")
def run(budget: int, dry_run: bool, work_orders_dir: str):
    """Execute pending work orders with budget enforcement."""
    console.print("[bold blue]Code Monkeys Factory :: Oracle Run[/bold blue]")
    
    cmd = [sys.executable, "scripts/oracle_executor.py", "--budget", str(budget)]
    
    if dry_run:
        cmd.append("--dry-run")
    
    cmd.extend(["--work-orders-dir", work_orders_dir])
    
    result = subprocess.run(cmd, capture_output=False)
    
    raise SystemExit(result.returncode)


@oracle.command()
def status():
    """Show current work order queue status."""
    console.print("[bold blue]Code Monkeys Factory :: Oracle Status[/bold blue]")
    
    work_orders_dir = Path("nexus/work_orders")
    
    if not work_orders_dir.exists():
        console.print("[yellow]No work orders directory found.[/yellow]")
        return
    
    import json
    
    pending = 0
    completed = 0
    failed = 0
    
    for wo_file in work_orders_dir.glob("*.json"):
        if wo_file.name.startswith("_"):
            continue
        with open(wo_file) as f:
            wo = json.load(f)
        status = wo.get("status", "pending")
        if status == "pending":
            pending += 1
        elif status == "completed":
            completed += 1
        elif status == "failed":
            failed += 1
    
    console.print(f"\n[bold]Work Order Queue[/bold]")
    console.print(f"  Pending:   {pending}")
    console.print(f"  Completed: {completed}")
    console.print(f"  Failed:    {failed}")
    console.print(f"  Total:     {pending + completed + failed}")


if __name__ == "__main__":
    oracle()
