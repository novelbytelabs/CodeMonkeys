import click
import json
import os
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()

@click.group()
def fleet():
    """Manage the Product Fleet."""
    pass

@fleet.command()
def list():
    """List all registered products."""
    products_file = Path("dash/products.json")
    if not products_file.exists():
        console.print("[bold red]dash/products.json not found![/bold red]")
        return

    try:
        data = json.loads(products_file.read_text())
        products = data.get("products", [])
        
        table = Table(title=f"Code Monkeys Fleet ({len(products)} products)")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="magenta")
        table.add_column("Owner", style="green")
        table.add_column("Status", style="yellow")
        
        for p in products:
            table.add_row(
                p.get("product_id", "N/A"),
                p.get("display_name", "N/A"),
                p.get("owner", "N/A"),
                p.get("status", "N/A")
            )
            
        console.print(table)
        
    except Exception as e:
        console.print(f"[bold red]Error reading fleet:[/bold red] {e}")

@fleet.command()
def status():
    """Show detailed status (mock for now)."""
    # Just reusing list for now, will enhance in Phase 4
    ctx = click.get_current_context()
    ctx.invoke(list)
