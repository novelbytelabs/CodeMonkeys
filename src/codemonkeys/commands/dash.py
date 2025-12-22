import click
import sys
import subprocess
from rich.console import Console

console = Console()

@click.command()
@click.option('--port', default=8080, help='Port to serve on')
def dash(port):
    """Serve the Dash interface."""
    console.print(f"[bold blue]Code Monkeys Factory :: Dash available at http://localhost:{port}/dash/index.html[/bold blue]")
    
    try:
        # Use python's builtin http.server as before
        subprocess.run(["python", "-m", "http.server", str(port)], check=False)
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Dash server stopped.[/bold yellow]")
    except Exception as e:
        console.print(f"[bold red]Error running Dash:[/bold red] {e}")
        sys.exit(1)
