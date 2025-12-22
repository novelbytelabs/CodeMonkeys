import click
from rich.console import Console
from codemonkeys.commands.dash import dash
from codemonkeys.commands.run import run
from codemonkeys.commands.silverback import silverback
from codemonkeys.commands.nexus import nexus
from codemonkeys.commands.fleet import fleet
from codemonkeys.commands.dossier import dossier
from codemonkeys.commands.ship import ship

console = Console()

@click.group()
def cli():
    """Code Monkeys Factory Control Plane."""
    pass

cli.add_command(dash)
cli.add_command(run)
cli.add_command(silverback)
cli.add_command(nexus)
cli.add_command(fleet)
cli.add_command(dossier)
cli.add_command(ship)

if __name__ == "__main__":
    cli()
