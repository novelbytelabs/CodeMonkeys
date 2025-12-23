"""Dash commands - portfolio dashboard and index management."""
import subprocess
import sys
from pathlib import Path

import click
from rich.console import Console

console = Console()


@click.group()
def dash():
    """Dash - portfolio dashboard and index management."""
    pass


@dash.command()
@click.option('--port', default=8080, help='Port to serve on')
def serve(port):
    """Serve the Dash interface."""
    console.print(
        f"[bold blue]Code Monkeys Factory :: Dash[/bold blue]"
    )
    console.print(f"Available at http://localhost:{port}/dash/index.html")

    try:
        subprocess.run([sys.executable, "-m", "http.server", str(port)], check=False)
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Dash server stopped.[/bold yellow]")
    except Exception as e:
        console.print(f"[bold red]Error running Dash:[/bold red] {e}")
        sys.exit(1)


@dash.command()
@click.option('--all', 'refresh_all', is_flag=True, default=True, help='Refresh all indices')
@click.option('--science', is_flag=True, help='Only refresh science index')
@click.option('--output', type=click.Path(), default=None, help='Alternate output path')
def refresh(refresh_all, science, output):
    """Regenerate Dash index artifacts."""
    console.print("[bold blue]Code Monkeys Factory :: Dash Refresh[/bold blue]")

    failed = False

    # Science index
    if refresh_all or science:
        console.print("\n[bold]Generating science_index.json...[/bold]")
        cmd = [sys.executable, "scripts/generate_science_index.py"]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            console.print(f"[red]✗ Science index generation failed[/red]")
            console.print(result.stderr)
            failed = True
        else:
            console.print(f"[green]✓ Science index generated[/green]")
            # Show output
            for line in result.stdout.strip().split('\n'):
                if line:
                    console.print(f"  {line}")

    # Future: Add more indexers here
    # if refresh_all or other_flag:
    #     run_other_indexer()

    if failed:
        console.print("\n[red]✗ Refresh failed[/red]")
        sys.exit(1)
    else:
        console.print("\n[green]✓ All indices refreshed[/green]")


if __name__ == "__main__":
    dash()
