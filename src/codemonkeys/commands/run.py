import click
import sys
import subprocess
from rich.console import Console

console = Console()

@click.command()
@click.argument('product_id')
@click.option('--path', default=None, help='Path to product directory')
@click.option('--test-path', default=None, help='Path to tests')
@click.option('--ci', is_flag=True, help='Run in CI mode')
def run(product_id, path, test_path, ci):
    """Run tests and generate artifact for a product."""
    console.print(f"[bold blue]Code Monkeys Factory :: Running {product_id}[/bold blue]")
    
    cmd = ["python", "scripts/generate_run_report.py", product_id]
    if path:
        cmd.extend(["--path", path])
    if test_path:
        cmd.extend(["--test-path", test_path])
    if ci:
        cmd.append("--ci")
        
    try:
        # We delegate to the existing robust script
        result = subprocess.run(cmd, check=False)
        if result.returncode != 0:
            sys.exit(result.returncode)
    except Exception as e:
        console.print(f"[bold red]Error running product:[/bold red] {e}")
        sys.exit(1)
